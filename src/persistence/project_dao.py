"""Operaciones de inserción para proyectos."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.project import Project


class ProjectDAO:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, project: Project) -> int:
        with self._connection:
            cursor = self._connection.execute(
                "INSERT INTO projects (name) VALUES (?)",
                (project.name,),
            )
        if cursor.lastrowid is None:
            raise sqlite3.DatabaseError(
                "No se obtuvo el identificador del proyecto."
            )
        return cursor.lastrowid
