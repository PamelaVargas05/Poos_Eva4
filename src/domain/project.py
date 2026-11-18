"""Representa un proyecto y los registros de trabajo que recibe."""

from __future__ import annotations

from .work_record import WorkRecord


class Project:
    def __init__(self, name: str, project_id: int | None = None) -> None:
        self.__name = self._validate_name(name)
        self.__project_id = self._validate_id(
            project_id, "El identificador del proyecto debe ser positivo."
        )
        self.__work_records: list[WorkRecord] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def project_id(self) -> int | None:
        return self.__project_id

    def update_name(self, name: str) -> None:
        self.__name = self._validate_name(name)

    def assign_project_id(self, project_id: int) -> None:
        if self.__project_id is not None:
            raise ValueError("El identificador del proyecto ya fue asignado.")
        self.__project_id = self._validate_id(
            project_id, "El identificador del proyecto debe ser positivo."
        )

    def add_work_record(self, work_record: WorkRecord) -> None:
        if not isinstance(work_record, WorkRecord):
            raise TypeError("Solo se pueden asociar objetos WorkRecord.")
        if self.__project_id is None or work_record.project_id != self.__project_id:
            raise ValueError(
                "El registro de trabajo debe corresponder a este proyecto persistido."
            )
        if any(
            current is work_record
            or (
                work_record.work_record_id is not None
                and current.work_record_id == work_record.work_record_id
            )
            for current in self.__work_records
        ):
            raise ValueError("El registro ya está asociado a este proyecto.")
        self.__work_records.append(work_record)

    def get_work_records(self) -> tuple[WorkRecord, ...]:
        return tuple(self.__work_records)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        return name

    @staticmethod
    def _validate_id(value: int | None, message: str) -> int | None:
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value <= 0
        ):
            raise ValueError(message)
        return value
