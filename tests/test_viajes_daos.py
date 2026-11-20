import unittest
from datetime import date
from decimal import Decimal

from src.viajes.domain import Destination, TravelPackage, User
from src.viajes.errors import AvailabilityError
from src.viajes.persistence.destination_dao import DestinationDAO
from src.viajes.persistence.package_dao import TravelPackageDAO
from src.viajes.persistence.reservation_dao import ReservationDAO
from src.viajes.persistence.user_dao import UserDAO


class FakeCursor:
    def __init__(self) -> None:
        self.statements: list[tuple[str, object]] = []
        self.fetchone_results: list[object] = []
        self.fetchall_results: list[list[object]] = []
        self.lastrowid = 41
        self.rowcount = 1
        self.closed = False

    def execute(self, statement: str, parameters: object = None) -> None:
        self.statements.append((statement, parameters))

    def executemany(self, statement: str, parameters: object) -> None:
        self.statements.append((statement, parameters))

    def fetchone(self) -> object:
        return self.fetchone_results.pop(0)

    def fetchall(self) -> list[object]:
        return self.fetchall_results.pop(0)

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self._cursor = cursor
        self.commits = 0
        self.rollbacks = 0
        self.started_transactions = 0
        self.closed = False

    def cursor(self, dictionary: bool = False) -> FakeCursor:
        self.dictionary_mode = dictionary
        return self._cursor

    def commit(self) -> None:
        self.commits += 1

    def start_transaction(self) -> None:
        self.started_transactions += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def close(self) -> None:
        self.closed = True


class ViajesDAOTests(unittest.TestCase):
    def test_destination_insert_uses_parameters_and_returns_generated_id(self) -> None:
        cursor = FakeCursor()
        connection = FakeConnection(cursor)
        destination = Destination("Valdivia", "Chile")

        destination_id = DestinationDAO(lambda: connection).create(destination)

        self.assertEqual(destination_id, 41)
        self.assertEqual(destination.destination_id, 41)
        self.assertEqual(
            cursor.statements[0][1],
            ("Valdivia", "Chile", ""),
        )
        self.assertIn("%s", cursor.statements[0][0])
        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.started_transactions, 1)

    def test_destination_update_and_delete_use_parameterized_queries(self) -> None:
        updated_cursor = FakeCursor()
        updated_connection = FakeConnection(updated_cursor)
        DestinationDAO(lambda: updated_connection).update(
            4, Destination("Puerto Varas", "Chile", "Lagos")
        )
        self.assertIn("%s", updated_cursor.statements[0][0])
        self.assertEqual(
            updated_cursor.statements[0][1],
            ("Puerto Varas", "Chile", "Lagos", 4),
        )
        self.assertEqual(updated_connection.commits, 1)

        deleted_cursor = FakeCursor()
        deleted_connection = FakeConnection(deleted_cursor)
        DestinationDAO(lambda: deleted_connection).delete(4)
        self.assertEqual(deleted_cursor.statements[0][1], (4,))
        self.assertEqual(deleted_connection.commits, 1)

    def test_package_insert_links_multiple_destinations_in_one_transaction(self) -> None:
        cursor = FakeCursor()
        cursor.fetchall_results.append(
            [{"destination_id": 1}, {"destination_id": 2}]
        )
        connection = FakeConnection(cursor)
        package = TravelPackage(
            "Sur",
            "",
            date(2027, 2, 1),
            date(2027, 2, 5),
            Decimal("900.00"),
            12,
            [1, 2],
        )

        package_id = TravelPackageDAO(lambda: connection).create(package)

        self.assertEqual(package_id, 41)
        self.assertEqual(package.package_id, 41)
        self.assertEqual(len(cursor.statements), 3)
        self.assertEqual(cursor.statements[-1][1], [(41, 1), (41, 2)])
        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.started_transactions, 1)

    def test_package_destination_query_returns_related_objects(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.append({"package_id": 41})
        cursor.fetchall_results.append(
            [{"destination_id": 1, "name": "Valdivia", "country": "Chile", "description": ""}]
        )
        connection = FakeConnection(cursor)

        destinations = TravelPackageDAO(lambda: connection).get_destinations(41)

        self.assertEqual(len(destinations), 1)
        self.assertEqual(destinations[0].name, "Valdivia")
        self.assertEqual(cursor.statements[1][1], (41,))

    def test_package_update_replaces_links_atomically(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.append({"package_id": 41})
        cursor.fetchall_results.append([{"destination_id": 2}])
        connection = FakeConnection(cursor)
        package = TravelPackage(
            "Nuevo sur",
            "",
            date(2027, 3, 1),
            date(2027, 3, 4),
            "120.00",
            5,
            [2],
        )

        TravelPackageDAO(lambda: connection).update(41, package)

        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.started_transactions, 1)
        self.assertEqual(cursor.statements[-1][1], [(41, 2)])
        self.assertIn("DELETE FROM package_destinations", cursor.statements[-2][0])

    def test_user_registration_persists_only_the_password_hash(self) -> None:
        cursor = FakeCursor()
        connection = FakeConnection(cursor)
        user = User("Pamela Vargas", "pamela@example.com")
        password_hash = f"pbkdf2_sha256$600000${'a' * 32}${'b' * 64}"

        UserDAO(lambda: connection).create(user, password_hash)

        self.assertEqual(user.user_id, 41)
        self.assertEqual(cursor.statements[0][1], (
            "Pamela Vargas",
            "pamela@example.com",
            password_hash,
        ))
        self.assertNotIn("plain-text-password", str(cursor.statements))
        self.assertEqual(connection.commits, 1)

    def test_credentials_lookup_returns_hash_without_selecting_it_for_profiles(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.append(
            {
                "user_id": 41,
                "full_name": "Pamela Vargas",
                "email": "pamela@example.com",
                "role": "customer",
                "password_hash": "encoded-hash",
            }
        )
        connection = FakeConnection(cursor)

        credentials = UserDAO(lambda: connection).get_credentials_by_email(
            " PAMELA@example.com "
        )

        self.assertIsNotNone(credentials)
        self.assertEqual(credentials[0].email, "pamela@example.com")
        self.assertEqual(credentials[1], "encoded-hash")
        self.assertEqual(cursor.statements[0][1], ("pamela@example.com",))
        self.assertIn("password_hash", cursor.statements[0][0])

    def test_reservation_decrements_inventory_and_persists_price_snapshot(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.extend(
            [
                {"user_id": 7},
                {
                    "package_id": 8,
                    "start_date": date(2027, 2, 1),
                    "unit_price": Decimal("99.50"),
                    "available_slots": 4,
                },
            ]
        )
        connection = FakeConnection(cursor)

        reservation = ReservationDAO(lambda: connection).create(7, 8, 2)

        self.assertEqual(reservation.reservation_id, 41)
        self.assertEqual(reservation.total_price, Decimal("199.00"))
        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.started_transactions, 1)
        self.assertEqual(
            cursor.statements[2][1],
            (2, 8, 2),
        )
        self.assertEqual(
            cursor.statements[3][1],
            (7, 8, 2, Decimal("99.50"), Decimal("199.00")),
        )

    def test_reservation_over_availability_rolls_back_without_inserting(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.extend(
            [
                {"user_id": 7},
                {
                    "package_id": 8,
                    "start_date": date(2027, 2, 1),
                    "unit_price": Decimal("99.50"),
                    "available_slots": 1,
                },
            ]
        )
        connection = FakeConnection(cursor)

        with self.assertRaises(AvailabilityError):
            ReservationDAO(lambda: connection).create(7, 8, 2)

        self.assertEqual(connection.commits, 0)
        self.assertEqual(connection.rollbacks, 1)
        self.assertEqual(connection.started_transactions, 1)
        self.assertEqual(len(cursor.statements), 2)

    def test_cancelling_reservation_restores_availability_in_one_transaction(self) -> None:
        cursor = FakeCursor()
        cursor.fetchone_results.append(
            {
                "reservation_id": 3,
                "user_id": 7,
                "package_id": 8,
                "travelers": 2,
                "status": "confirmed",
            }
        )
        connection = FakeConnection(cursor)

        ReservationDAO(lambda: connection).cancel(3)

        self.assertEqual(connection.commits, 1)
        self.assertEqual(connection.started_transactions, 1)
        self.assertIn("available_slots + %s", cursor.statements[1][0])
        self.assertEqual(cursor.statements[1][1], (2, 8))
        self.assertEqual(cursor.statements[2][1], ("cancelled", 3))


if __name__ == "__main__":
    unittest.main()
