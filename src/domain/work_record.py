"""Representa las horas de un empleado en un proyecto."""

from datetime import date
from math import isfinite


class WorkRecord:
    def __init__(
        self,
        employee_id: int,
        project_id: int,
        work_date: date,
        hours: float,
        work_record_id: int | None = None,
    ) -> None:
        self.__employee_id = self._validate_id(
            employee_id, "El identificador del empleado debe ser positivo."
        )
        self.__project_id = self._validate_id(
            project_id, "El identificador del proyecto debe ser positivo."
        )
        self.__work_date = self._validate_work_date(work_date)
        self.__hours = self._validate_hours(hours)
        self.__work_record_id = (
            None
            if work_record_id is None
            else self._validate_id(
                work_record_id, "El identificador del registro debe ser positivo."
            )
        )

    @property
    def employee_id(self) -> int:
        return self.__employee_id

    @property
    def project_id(self) -> int:
        return self.__project_id

    @property
    def work_date(self) -> date:
        return self.__work_date

    @property
    def hours(self) -> float:
        return self.__hours

    @property
    def work_record_id(self) -> int | None:
        return self.__work_record_id

    def update_work_date(self, work_date: date) -> None:
        self.__work_date = self._validate_work_date(work_date)

    def update_hours(self, hours: float) -> None:
        self.__hours = self._validate_hours(hours)

    def assign_work_record_id(self, work_record_id: int) -> None:
        if self.__work_record_id is not None:
            raise ValueError("El identificador del registro ya fue asignado.")
        self.__work_record_id = self._validate_id(
            work_record_id, "El identificador del registro debe ser positivo."
        )

    @staticmethod
    def _validate_id(value: int | None, message: str) -> int:
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
        ):
            raise ValueError(message)
        return value

    @staticmethod
    def _validate_work_date(work_date: date) -> date:
        if type(work_date) is not date:
            raise ValueError("La fecha del registro debe ser una fecha válida.")
        return work_date

    @staticmethod
    def _validate_hours(hours: float) -> float:
        if (
            isinstance(hours, bool)
            or not isinstance(hours, (int, float))
            or not isfinite(hours)
            or hours <= 0
        ):
            raise ValueError("Las horas registradas deben ser mayores que cero.")
        return float(hours)
