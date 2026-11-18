"""Representa un departamento y los empleados que tiene asociados."""

from __future__ import annotations

from .employee import Employee


class Department:
    def __init__(self, name: str, department_id: int | None = None) -> None:
        self.__name = self._validate_name(name)
        self.__department_id = self._validate_id(
            department_id, "El identificador del departamento debe ser positivo."
        )
        self.__employees: list[Employee] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def department_id(self) -> int | None:
        return self.__department_id

    def update_name(self, name: str) -> None:
        self.__name = self._validate_name(name)

    def assign_department_id(self, department_id: int) -> None:
        if self.__department_id is not None:
            raise ValueError("El identificador del departamento ya fue asignado.")
        self.__department_id = self._validate_id(
            department_id, "El identificador del departamento debe ser positivo."
        )

    def add_employee(self, employee: Employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Solo se pueden asociar objetos Employee.")
        if (
            self.__department_id is None
            or employee.department_id != self.__department_id
        ):
            raise ValueError(
                "El empleado debe pertenecer a este departamento persistido."
            )
        if any(
            current is employee
            or (
                employee.employee_id is not None
                and current.employee_id == employee.employee_id
            )
            for current in self.__employees
        ):
            raise ValueError("El empleado ya está asociado a este departamento.")
        self.__employees.append(employee)

    def get_employees(self) -> tuple[Employee, ...]:
        return tuple(self.__employees)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre del departamento no puede estar vacío.")
        return name

    @staticmethod
    def _validate_id(value: int | None, message: str) -> int | None:
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value <= 0
        ):
            raise ValueError(message)
        return value
