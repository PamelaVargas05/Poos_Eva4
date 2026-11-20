"""Reserva confirmada, con precio unitario inmutable de referencia."""

from datetime import datetime
from decimal import Decimal

from ._validation import positive_decimal, positive_id
from .pricing import MAX_TRAVELERS, calculate_total_price


class Reservation:
    __slots__ = (
        "__reservation_id",
        "__user_id",
        "__package_id",
        "__booked_at",
        "__travelers",
        "__unit_price",
        "__total_price",
        "__status",
    )

    def __init__(
        self,
        user_id: int,
        package_id: int,
        travelers: int,
        unit_price: Decimal | int | float | str,
        status: str = "confirmed",
        reservation_id: int | None = None,
        booked_at: datetime | None = None,
    ) -> None:
        self.__reservation_id = (
            positive_id(reservation_id, "La reserva")
            if reservation_id is not None
            else None
        )
        self.__user_id = positive_id(user_id, "El usuario")
        self.__package_id = positive_id(package_id, "El paquete")
        if (
            isinstance(travelers, bool)
            or not isinstance(travelers, int)
            or not 1 <= travelers <= MAX_TRAVELERS
        ):
            raise ValueError("La cantidad de viajeros está fuera del rango permitido.")
        self.__travelers = travelers
        self.__unit_price = positive_decimal(unit_price, "El precio unitario")
        self.__total_price = calculate_total_price(
            self.__unit_price, self.__travelers
        )
        if not isinstance(status, str) or status not in {"confirmed", "cancelled"}:
            raise ValueError("El estado de la reserva no es válido.")
        self.__status = status
        self.__booked_at = booked_at or datetime.now()

    @property
    def reservation_id(self) -> int | None:
        return self.__reservation_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def package_id(self) -> int:
        return self.__package_id

    @property
    def travelers(self) -> int:
        return self.__travelers

    @property
    def unit_price(self) -> Decimal:
        return self.__unit_price

    @property
    def total_price(self) -> Decimal:
        return self.__total_price

    @property
    def status(self) -> str:
        return self.__status

    @property
    def booked_at(self) -> datetime:
        return self.__booked_at

    def assign_id(self, reservation_id: int) -> None:
        if self.__reservation_id is not None:
            raise ValueError("La reserva ya tiene identificador.")
        self.__reservation_id = positive_id(reservation_id, "La reserva")

    def cancel(self) -> None:
        if self.__status == "cancelled":
            raise ValueError("La reserva ya está cancelada.")
        self.__status = "cancelled"
