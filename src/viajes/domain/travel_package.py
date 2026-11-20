"""Paquete turístico y cálculo único de costos."""

from datetime import date
from decimal import Decimal

from ._validation import positive_decimal, positive_id, required_text, valid_date
from .pricing import MAX_TRAVELERS, calculate_total_price


class TravelPackage:
    __slots__ = (
        "__package_id",
        "__name",
        "__description",
        "__start_date",
        "__end_date",
        "__unit_price",
        "__available_slots",
        "__destination_ids",
    )

    def __init__(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        unit_price: Decimal | int | float | str,
        available_slots: int,
        destination_ids: tuple[int, ...] | list[int],
        package_id: int | None = None,
    ) -> None:
        self.__package_id = (
            positive_id(package_id, "El paquete") if package_id is not None else None
        )
        self.__name = required_text(name, "El nombre", 160)
        if not isinstance(description, str):
            raise ValueError("La descripción debe ser texto.")
        self.__description = description.strip()
        self.__start_date = valid_date(start_date, "La fecha de inicio")
        self.__end_date = valid_date(end_date, "La fecha de término")
        if self.__end_date < self.__start_date:
            raise ValueError("La fecha de término no puede preceder al inicio.")
        self.__unit_price = positive_decimal(unit_price, "El precio")
        if (
            isinstance(available_slots, bool)
            or not isinstance(available_slots, int)
            or not 0 <= available_slots <= MAX_TRAVELERS
        ):
            raise ValueError("La disponibilidad debe ser un entero no negativo.")
        self.__available_slots = available_slots
        ids = tuple(positive_id(item, "El destino") for item in destination_ids)
        if not ids:
            raise ValueError("El paquete debe incluir al menos un destino.")
        if len(set(ids)) != len(ids):
            raise ValueError("El paquete no puede repetir destinos.")
        self.__destination_ids = ids

    @property
    def package_id(self) -> int | None:
        return self.__package_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def start_date(self) -> date:
        return self.__start_date

    @property
    def end_date(self) -> date:
        return self.__end_date

    @property
    def duration_days(self) -> int:
        return (self.__end_date - self.__start_date).days + 1

    @property
    def unit_price(self) -> Decimal:
        return self.__unit_price

    @property
    def available_slots(self) -> int:
        return self.__available_slots

    @property
    def destination_ids(self) -> tuple[int, ...]:
        return self.__destination_ids

    def calculate_total(self, travelers: int) -> Decimal:
        return calculate_total_price(self.__unit_price, travelers)

    def assign_id(self, package_id: int) -> None:
        if self.__package_id is not None:
            raise ValueError("El paquete ya tiene identificador.")
        self.__package_id = positive_id(package_id, "El paquete")
