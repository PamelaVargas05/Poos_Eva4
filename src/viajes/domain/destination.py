"""Destino turístico."""

from ._validation import required_text, positive_id


class Destination:
    __slots__ = ("__destination_id", "__name", "__country", "__description")

    def __init__(
        self,
        name: str,
        country: str,
        description: str = "",
        destination_id: int | None = None,
    ) -> None:
        self.__destination_id = (
            positive_id(destination_id, "El destino")
            if destination_id is not None
            else None
        )
        self.__name = required_text(name, "El nombre", 120)
        self.__country = required_text(country, "El país", 100)
        if not isinstance(description, str):
            raise ValueError("La descripción debe ser texto.")
        self.__description = description.strip()

    @property
    def destination_id(self) -> int | None:
        return self.__destination_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def country(self) -> str:
        return self.__country

    @property
    def description(self) -> str:
        return self.__description

    def assign_id(self, destination_id: int) -> None:
        if self.__destination_id is not None:
            raise ValueError("El destino ya tiene identificador.")
        self.__destination_id = positive_id(destination_id, "El destino")

    def update(self, name: str, country: str, description: str) -> None:
        updated = Destination(name, country, description, self.__destination_id)
        self.__name = updated.name
        self.__country = updated.country
        self.__description = updated.description
