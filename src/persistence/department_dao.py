"""Operaciones de inserción para departamentos."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.department import Department


class DepartmentDAO:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, department: Department) -> int:
        with self._connection:
            cursor = self._connection.execute(
                "INSERT INTO departments (name) VALUES (?)",
                (department.name,),
            )
        if cursor.lastrowid is None:
            raise sqlite3.DatabaseError(
                "No se obtuvo el identificador del departamento."
            )
        return cursor.lastrowid
