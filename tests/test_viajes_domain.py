import unittest
from datetime import date
from decimal import Decimal

from src.viajes.domain import Destination, Reservation, TravelPackage, User


class ViajesDomainTests(unittest.TestCase):
    def test_package_requires_destinations_and_calculates_total_once(self) -> None:
        with self.assertRaisesRegex(ValueError, "al menos un destino"):
            TravelPackage("Ruta", "", date(2027, 1, 1), date(2027, 1, 2), 10, 4, [])

        package = TravelPackage(
            " Ruta ",
            "",
            date(2027, 1, 1),
            date(2027, 1, 3),
            "1250.50",
            4,
            [1, 2],
        )
        self.assertEqual(package.name, "Ruta")
        self.assertEqual(package.duration_days, 3)
        self.assertEqual(package.calculate_total(2), Decimal("2501.00"))
        with self.assertRaises(ValueError):
            package.calculate_total(0)
        sold_out = TravelPackage(
            "Agotado", "", date(2027, 1, 1), date(2027, 1, 1), 1, 0, [1]
        )
        self.assertEqual(sold_out.available_slots, 0)

    def test_rejects_invalid_package_dates_and_amounts(self) -> None:
        with self.assertRaisesRegex(ValueError, "término"):
            TravelPackage(
                "Ruta", "", date(2027, 2, 1), date(2027, 1, 1), 1, 1, [1]
            )
        with self.assertRaisesRegex(ValueError, "precio"):
            TravelPackage(
                "Ruta", "", date(2027, 1, 1), date(2027, 1, 2), 0, 1, [1]
            )
        with self.assertRaisesRegex(ValueError, "rango monetario"):
            TravelPackage(
                "Ruta", "", date(2027, 1, 1), date(2027, 1, 2), "0.001", 1, [1]
            )

    def test_user_normalizes_email_and_never_accepts_plain_empty_credential(self) -> None:
        user = User("Pamela Vargas", " PAMELA@example.com ")
        self.assertEqual(user.email, "pamela@example.com")
        self.assertEqual(user.role, "customer")
        with self.assertRaises(ValueError):
            User("Pamela Vargas", "invalido", "hash")

    def test_reservation_preserves_price_snapshot_and_cancels_once(self) -> None:
        reservation = Reservation(1, 2, 3, "12.50")
        self.assertEqual(reservation.total_price, Decimal("37.50"))
        reservation.cancel()
        self.assertEqual(reservation.status, "cancelled")
        with self.assertRaisesRegex(ValueError, "cancelada"):
            reservation.cancel()

    def test_destination_validation_and_generated_id_assignment(self) -> None:
        destination = Destination("Valdivia", "Chile")
        destination.assign_id(7)
        self.assertEqual(destination.destination_id, 7)
        with self.assertRaises(ValueError):
            destination.assign_id(8)
        with self.assertRaises(ValueError):
            Destination(" ", "Chile")


if __name__ == "__main__":
    unittest.main()
