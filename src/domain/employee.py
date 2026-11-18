"""Representa un empleado y sus registros de trabajo asociados."""

from __future__ import annotations

from .work_record import WorkRecord


class Employee:
    def __init__(
        self,
        name: str,
        department_id: int,
        employee_id: int | None = None,
    ) -> None:
        self.__name = self._validate_name(name)
        self.__department_id = self._validate_id(
            department_id, "El identificador del departamento debe ser positivo."
        )
        self.__employee_id = (
            None
            if employee_id is None
            else self._validate_id(
                employee_id, "El identificador del empleado debe ser positivo."
            )
        )
        self.__work_records: list[WorkRecord] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def department_id(self) -> int:
        return self.__department_id

    @property
    def employee_id(self) -> int | None:
        return self.__employee_id

    def update_name(self, name: str) -> None:
        self.__name = self._validate_name(name)

    def assign_employee_id(self, employee_id: int) -> None:
        if self.__employee_id is not None:
            raise ValueError("El identificador del empleado ya fue asignado.")
        self.__employee_id = self._validate_id(
            employee_id, "El identificador del empleado debe ser positivo."
        )

    def add_work_record(self, work_record: WorkRecord) -> None:
        if not isinstance(work_record, WorkRecord):
            raise TypeError("Solo se pueden asociar objetos WorkRecord.")
        if self.__employee_id is None or work_record.employee_id != self.__employee_id:
            raise ValueError(
                "El registro de trabajo debe corresponder a este empleado persistido."
            )
        if any(
            current is work_record
            or (
                work_record.work_record_id is not None
                and current.work_record_id == work_record.work_record_id
            )
            for current in self.__work_records
        ):
            raise ValueError("El registro ya está asociado a este empleado.")
        self.__work_records.append(work_record)

    def get_work_records(self) -> tuple[WorkRecord, ...]:
        return tuple(self.__work_records)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        return name

    @staticmethod
    def _validate_id(value: int | None, message: str) -> int:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            raise ValueError(message)
        return value
