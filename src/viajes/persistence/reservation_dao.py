"""Reservas con control transaccional de disponibilidad."""

from datetime import date, datetime
from typing import Callable

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict

from src.persistence.viajes_connection import get_connection
from src.viajes.domain import Reservation
from src.viajes.errors import AvailabilityError, NotFoundError
from ._common import database_cursor, rollback


class ReservationDAO:
    def __init__(
        self, connection_factory: Callable[[], MySQLConnection] = get_connection
    ) -> None:
        self._connection_factory = connection_factory

    @staticmethod
    def _from_row(row: dict[str, object]) -> Reservation:
        booked_at = row["booked_at"]
        if not isinstance(booked_at, datetime):
            raise RuntimeError("La base de datos devolvió una fecha de reserva inválida.")
        return Reservation(
            user_id=int(row["user_id"]),
            package_id=int(row["package_id"]),
            travelers=int(row["travelers"]),
            unit_price=str(row["unit_price"]),
            status=str(row["status"]),
            reservation_id=int(row["reservation_id"]),
            booked_at=booked_at,
        )

    @staticmethod
    def _fetch_reservation(
        cursor: MySQLCursorDict, reservation_id: int
    ) -> dict[str, object]:
        cursor.execute(
            "SELECT reservation_id, user_id, package_id, booked_at, travelers, "
            "unit_price, status FROM reservations "
            "WHERE reservation_id = %s FOR UPDATE",
            (reservation_id,),
        )
        row = cursor.fetchone()
        if row is None:
            raise NotFoundError("No se encontró la reserva solicitada.")
        return row

    def create(self, user_id: int, package_id: int, travelers: int) -> Reservation:
        if (
            isinstance(travelers, bool)
            or not isinstance(travelers, int)
            or travelers <= 0
        ):
            raise ValueError("La cantidad de viajeros debe ser un entero positivo.")
        with database_cursor(self._connection_factory, dictionary=True) as (
            connection,
            cursor,
        ):
            try:
                connection.start_transaction()
                cursor.execute(
                    "SELECT user_id FROM users WHERE user_id = %s",
                    (user_id,),
                )
                if cursor.fetchone() is None:
                    raise NotFoundError("No se encontró el usuario solicitado.")
                cursor.execute(
                    "SELECT package_id, start_date, unit_price, available_slots "
                    "FROM travel_packages WHERE package_id = %s FOR UPDATE",
                    (package_id,),
                )
                package = cursor.fetchone()
                if package is None:
                    raise NotFoundError("No se encontró el paquete solicitado.")
                start_date = package["start_date"]
                if not isinstance(start_date, date) or start_date <= date.today():
                    raise ValueError("No se puede reservar un paquete que ya comenzó.")
                available = int(package["available_slots"])
                if travelers > available:
                    raise AvailabilityError(
                        "La cantidad solicitada supera la disponibilidad del paquete."
                    )
                unit_price = str(package["unit_price"])
                reservation = Reservation(
                    user_id,
                    package_id,
                    travelers,
                    unit_price,
                )
                cursor.execute(
                    "UPDATE travel_packages SET available_slots = available_slots - %s "
                    "WHERE package_id = %s AND available_slots >= %s",
                    (travelers, package_id, travelers),
                )
                if cursor.rowcount != 1:
                    raise AvailabilityError(
                        "La disponibilidad del paquete cambió; inténtelo nuevamente."
                    )
                cursor.execute(
                    "INSERT INTO reservations "
                    "(user_id, package_id, travelers, unit_price, total_price, status) "
                    "VALUES (%s, %s, %s, %s, %s, 'confirmed')",
                    (
                        user_id,
                        package_id,
                        travelers,
                        reservation.unit_price,
                        reservation.total_price,
                    ),
                )
                reservation_id = int(cursor.lastrowid)
                connection.commit()
                reservation.assign_id(reservation_id)
                return reservation
            except Exception:
                rollback(connection)
                raise

    def get_by_id(self, reservation_id: int) -> Reservation:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT reservation_id, user_id, package_id, booked_at, travelers, "
                "unit_price, status FROM reservations WHERE reservation_id = %s",
                (reservation_id,),
            )
            row = cursor.fetchone()
        if row is None:
            raise NotFoundError("No se encontró la reserva solicitada.")
        return self._from_row(row)

    def list_by_user(self, user_id: int) -> list[Reservation]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT reservation_id, user_id, package_id, booked_at, travelers, "
                "unit_price, status FROM reservations WHERE user_id = %s "
                "ORDER BY booked_at DESC, reservation_id DESC",
                (user_id,),
            )
            return [self._from_row(row) for row in cursor.fetchall()]

    def list_all(self) -> list[Reservation]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT reservation_id, user_id, package_id, booked_at, travelers, "
                "unit_price, status FROM reservations "
                "ORDER BY booked_at DESC, reservation_id DESC"
            )
            return [self._from_row(row) for row in cursor.fetchall()]

    def update_status(self, reservation_id: int, status: str) -> None:
        if not isinstance(status, str) or status not in {"confirmed", "cancelled"}:
            raise ValueError("El estado de la reserva no es válido.")
        with database_cursor(self._connection_factory, dictionary=True) as (
            connection,
            cursor,
        ):
            try:
                connection.start_transaction()
                row = self._fetch_reservation(cursor, reservation_id)
                current = str(row["status"])
                if current == status:
                    connection.commit()
                    return
                travelers = int(row["travelers"])
                package_id = int(row["package_id"])
                if status == "cancelled":
                    cursor.execute(
                        "UPDATE travel_packages SET available_slots = "
                        "available_slots + %s WHERE package_id = %s",
                        (travelers, package_id),
                    )
                    if cursor.rowcount != 1:
                        raise NotFoundError("No se encontró el paquete de la reserva.")
                else:
                    cursor.execute(
                        "SELECT start_date, available_slots FROM travel_packages "
                        "WHERE package_id = %s FOR UPDATE",
                        (package_id,),
                    )
                    package = cursor.fetchone()
                    if package is None:
                        raise NotFoundError("No se encontró el paquete de la reserva.")
                    start_date = package["start_date"]
                    if not isinstance(start_date, date) or start_date <= date.today():
                        raise ValueError("No se puede reactivar una reserva ya iniciada.")
                    if int(package["available_slots"]) < travelers:
                        raise AvailabilityError(
                            "No hay disponibilidad para reactivar la reserva."
                        )
                    cursor.execute(
                        "UPDATE travel_packages SET available_slots = available_slots - %s "
                        "WHERE package_id = %s AND available_slots >= %s",
                        (travelers, package_id, travelers),
                    )
                    if cursor.rowcount != 1:
                        raise AvailabilityError(
                            "La disponibilidad cambió; inténtelo nuevamente."
                        )
                cursor.execute(
                    "UPDATE reservations SET status = %s WHERE reservation_id = %s",
                    (status, reservation_id),
                )
                connection.commit()
            except Exception:
                rollback(connection)
                raise

    def cancel(self, reservation_id: int) -> None:
        self.update_status(reservation_id, "cancelled")
