"""CRUD end-to-end optativo con datos identificados y limpieza por PK exacta."""

import os
import threading
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import date, timedelta
from decimal import Decimal

from mysql.connector.connection import MySQLConnection

from src.persistence.viajes_connection import get_connection
from src.viajes.auth import AuthenticationService
from src.viajes.domain import Destination, Reservation, TravelPackage
from src.viajes.errors import AvailabilityError, DuplicateRecordError, NotFoundError
from src.viajes.persistence.destination_dao import DestinationDAO
from src.viajes.persistence.package_dao import TravelPackageDAO
from src.viajes.persistence.reservation_dao import ReservationDAO
from src.viajes.persistence.schema import initialize_tables, verify_tables
from src.viajes.persistence.user_dao import UserDAO

RUN_INTEGRATION = os.environ.get("VIAJES_RUN_INTEGRATION_TESTS") == "1"


@unittest.skipUnless(
    RUN_INTEGRATION,
    "Defina VIAJES_RUN_INTEGRATION_TESTS=1 para usar MariaDB local.",
)
class ViajesMariaDBIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        verify_tables()

    def _cleanup_exactly(self, statement: str, identifier: int) -> None:
        def cleanup() -> None:
            with closing(get_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(statement, (identifier,))
                    connection.commit()

        self.addCleanup(cleanup)

    def test_connection_and_schema_are_ready_and_repeatable(self) -> None:
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT 1")
                self.assertEqual(cursor.fetchone()[0], 1)

        initialize_tables()
        initialize_tables()
        verify_tables()

    def test_real_crud_authentication_and_reservation_lifecycle(self) -> None:
        token = uuid.uuid4().hex
        destinations = DestinationDAO()
        packages = TravelPackageDAO()
        users = UserDAO()
        reservations = ReservationDAO()
        auth = AuthenticationService(users)

        destination = Destination(f"Test-{token}", "Chile", "Registro de integración")
        destination_id = destinations.create(destination)
        self._cleanup_exactly(
            "DELETE FROM destinations WHERE destination_id = %s", destination_id
        )
        self.assertEqual(destinations.get_by_id(destination_id).name, destination.name)
        self.assertIn(
            destination_id,
            {item.destination_id for item in destinations.list_all()},
        )
        updated_destination = Destination(
            f"Test-Updated-{token}", "Chile", "Destino actualizado"
        )
        destinations.update(destination_id, updated_destination)
        self.assertEqual(
            destinations.get_by_id(destination_id).name,
            updated_destination.name,
        )

        second_destination = Destination(f"Test-Second-{token}", "Chile")
        second_destination_id = destinations.create(second_destination)
        self._cleanup_exactly(
            "DELETE FROM destinations WHERE destination_id = %s",
            second_destination_id,
        )

        user = auth.register(
            "Integration Test",
            f"integration-{token}@example.test",
            f"Test-Password-{token}",
        )
        self.assertIsNotNone(user.user_id)
        assert user.user_id is not None
        user_id = user.user_id
        self._cleanup_exactly(
            "DELETE FROM users WHERE user_id = %s",
            user_id,
        )
        self.assertEqual(users.get_by_id(user_id).email, user.email)
        found_user = users.find_by_email(user.email)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.user_id, user_id)
        self.assertIn(user_id, {item.user_id for item in users.list_all()})
        with self.assertRaises(DuplicateRecordError):
            auth.register(
                "Duplicate Test",
                user.email,
                f"Test-Password-Again-{token}",
            )
        authenticated = auth.login(user.email, f"Test-Password-{token}")
        self.assertEqual(authenticated.role, "customer")
        with self.assertRaises(PermissionError):
            auth.require_role("admin")
        with self.assertRaises(ValueError):
            auth.login(user.email, "incorrect password")
        auth.logout()
        self.assertIsNone(auth.current_user)

        start = date.today() + timedelta(days=30)
        package = TravelPackage(
            f"Test Package {token}",
            "Paquete de prueba de integración",
            start,
            start + timedelta(days=2),
            Decimal("19.90"),
            4,
            [destination_id, second_destination_id],
        )
        package_id = packages.create(package)
        self._cleanup_exactly(
            "DELETE FROM travel_packages WHERE package_id = %s",
            package_id,
        )
        self.assertEqual(packages.get_by_id(package_id).name, package.name)
        self.assertIn(package_id, {item.package_id for item in packages.list_all()})
        self.assertEqual(
            {item.destination_id for item in packages.get_destinations(package_id)},
            {destination_id, second_destination_id},
        )
        with self.assertRaises(ValueError):
            destinations.delete(second_destination_id)

        updated_package = TravelPackage(
            f"Test Package Updated {token}",
            "Paquete actualizado",
            start + timedelta(days=1),
            start + timedelta(days=3),
            Decimal("20.00"),
            4,
            [destination_id],
        )
        packages.update(package_id, updated_package)
        current_package = packages.get_by_id(package_id)
        self.assertEqual(current_package.unit_price, Decimal("20.00"))
        self.assertEqual(current_package.destination_ids, (destination_id,))

        disposable_package = TravelPackage(
            f"Test Delete Package {token}",
            "Paquete desechable",
            start,
            start,
            Decimal("1.00"),
            1,
            [destination_id],
        )
        disposable_package_id = packages.create(disposable_package)
        self._cleanup_exactly(
            "DELETE FROM travel_packages WHERE package_id = %s",
            disposable_package_id,
        )
        packages.delete(disposable_package_id)
        with self.assertRaises(NotFoundError):
            packages.get_by_id(disposable_package_id)

        disposable_destination = Destination(f"Test Delete Destination {token}", "Chile")
        disposable_destination_id = destinations.create(disposable_destination)
        self._cleanup_exactly(
            "DELETE FROM destinations WHERE destination_id = %s",
            disposable_destination_id,
        )
        destinations.delete(disposable_destination_id)
        with self.assertRaises(NotFoundError):
            destinations.get_by_id(disposable_destination_id)

        reservation = reservations.create(user_id, package_id, 2)
        assert reservation.reservation_id is not None
        reservation_id = reservation.reservation_id
        self._cleanup_exactly(
            "DELETE FROM reservations WHERE reservation_id = %s",
            reservation_id,
        )
        self.assertEqual(reservation.total_price, Decimal("40.00"))
        self.assertEqual(packages.get_by_id(package_id).available_slots, 2)
        self.assertEqual(reservations.get_by_id(reservation_id).status, "confirmed")
        self.assertEqual(
            [item.reservation_id for item in reservations.list_by_user(user_id)],
            [reservation_id],
        )
        with self.assertRaises(AvailabilityError):
            reservations.create(user_id, package_id, 3)
        self.assertEqual(packages.get_by_id(package_id).available_slots, 2)

        reservations.cancel(reservation_id)
        self.assertEqual(packages.get_by_id(package_id).available_slots, 4)
        reservations.cancel(reservation_id)
        self.assertEqual(packages.get_by_id(package_id).available_slots, 4)
        reservations.update_status(reservation_id, "confirmed")
        self.assertEqual(packages.get_by_id(package_id).available_slots, 2)
        reservations.update_status(reservation_id, "cancelled")
        self.assertEqual(packages.get_by_id(package_id).available_slots, 4)

    def test_initial_admin_role_when_no_admin_exists(self) -> None:
        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT user_id FROM users WHERE role = 'admin' LIMIT 1")
                if cursor.fetchone() is not None:
                    self.skipTest("Ya existe un administrador; no se modifica.")

        token = uuid.uuid4().hex
        users = UserDAO()
        service = AuthenticationService(users)
        email = f"integration-admin-{token}@example.test"
        password = f"Admin-Password-{token}"
        admin = service.bootstrap_admin("Integration Admin", email, password)
        assert admin.user_id is not None
        admin_id = admin.user_id
        self._cleanup_exactly(
            "DELETE FROM users WHERE user_id = %s",
            admin_id,
        )

        session = AuthenticationService(users)
        logged_in = session.login(email, password)
        self.assertEqual(logged_in.role, "admin")
        self.assertEqual(session.require_role("admin").user_id, admin_id)

    def test_concurrent_reservations_cannot_take_the_last_slot(self) -> None:
        token = uuid.uuid4().hex
        destinations = DestinationDAO()
        packages = TravelPackageDAO()
        users = UserDAO()
        reservations = ReservationDAO()

        destination_id = destinations.create(
            Destination(f"Race-{token}", "Chile", "Prueba de concurrencia")
        )
        self._cleanup_exactly(
            "DELETE FROM destinations WHERE destination_id = %s", destination_id
        )
        user = AuthenticationService(users).register(
            "Concurrency Test",
            f"concurrency-{token}@example.test",
            f"Concurrency-Password-{token}",
        )
        assert user.user_id is not None
        user_id = user.user_id
        self._cleanup_exactly(
            "DELETE FROM users WHERE user_id = %s", user_id
        )

        start = date.today() + timedelta(days=30)
        package_id = packages.create(
            TravelPackage(
                f"Last Slot {token}",
                "Prueba controlada del último cupo",
                start,
                start + timedelta(days=2),
                Decimal("25.00"),
                1,
                [destination_id],
            )
        )
        self._cleanup_exactly(
            "DELETE FROM travel_packages WHERE package_id = %s", package_id
        )

        def cleanup_test_reservations() -> None:
            with closing(get_connection()) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(
                        "SELECT reservation_id FROM reservations "
                        "WHERE user_id = %s AND package_id = %s",
                        (user_id, package_id),
                    )
                    reservation_ids = [row[0] for row in cursor.fetchall()]
                    for reservation_id in reservation_ids:
                        cursor.execute(
                            "DELETE FROM reservations WHERE reservation_id = %s",
                            (reservation_id,),
                        )
                    connection.commit()

        self.addCleanup(cleanup_test_reservations)
        connections = [get_connection(), get_connection()]

        def close_connections() -> None:
            for connection in connections:
                connection.close()

        self.addCleanup(close_connections)
        self.assertNotEqual(id(connections[0]), id(connections[1]))
        connection_ids = []
        for connection in connections:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT CONNECTION_ID()")
                connection_ids.append(cursor.fetchone()[0])
        self.assertNotEqual(connection_ids[0], connection_ids[1])
        start_together = threading.Barrier(3)

        def reserve(
            connection: MySQLConnection,
        ) -> Reservation | AvailabilityError:
            start_together.wait(timeout=10)
            try:
                return ReservationDAO(lambda: connection).create(
                    user_id, package_id, 1
                )
            except AvailabilityError as error:
                return error

        with ThreadPoolExecutor(max_workers=2) as executor:
            attempts = [
                executor.submit(reserve, connection) for connection in connections
            ]
            start_together.wait(timeout=10)
            outcomes = [attempt.result(timeout=30) for attempt in attempts]

        confirmed = [item for item in outcomes if isinstance(item, Reservation)]
        unavailable = [
            item for item in outcomes if isinstance(item, AvailabilityError)
        ]
        self.assertEqual(len(confirmed), 1)
        self.assertEqual(len(unavailable), 1)

        reservation_id = confirmed[0].reservation_id
        assert reservation_id is not None
        self._cleanup_exactly(
            "DELETE FROM reservations WHERE reservation_id = %s", reservation_id
        )

        self.assertEqual(packages.get_by_id(package_id).available_slots, 0)
        user_reservations = reservations.list_by_user(user_id)
        self.assertEqual(len(user_reservations), 1)
        self.assertEqual(user_reservations[0].reservation_id, reservation_id)
        self.assertEqual(user_reservations[0].status, "confirmed")
        self.assertEqual(user_reservations[0].travelers, 1)
        self.assertGreaterEqual(packages.get_by_id(package_id).available_slots, 0)

        with closing(get_connection()) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(
                    "SELECT COUNT(*), COALESCE(SUM(travelers), 0) "
                    "FROM reservations WHERE package_id = %s AND status = 'confirmed'",
                    (package_id,),
                )
                confirmed_count, reserved_slots = cursor.fetchone()
        self.assertEqual(confirmed_count, 1)
        self.assertEqual(
            packages.get_by_id(package_id).available_slots + reserved_slots, 1
        )


if __name__ == "__main__":
    unittest.main()
