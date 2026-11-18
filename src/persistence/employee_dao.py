"""Operaciones de inserción para empleados de apoyo."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.employee import Employee


class EmployeeDAO:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, employee: Employee) -> int:
        with self._connection:
            cursor = self._connection.execute(
                """
                INSERT INTO employees (name, department_id)
                VALUES (?, ?)
                """,
                (employee.name, employee.department_id),
            )
        if cursor.lastrowid is None:
            raise sqlite3.DatabaseError(
                "No se obtuvo el identificador del empleado."
            )
        return cursor.lastrowid
