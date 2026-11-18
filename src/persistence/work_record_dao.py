"""Operaciones de inserción para registros de trabajo."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.work_record import WorkRecord


class WorkRecordDAO:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, work_record: WorkRecord) -> int:
        with self._connection:
            cursor = self._connection.execute(
                """
                INSERT INTO work_records (
                    employee_id,
                    project_id,
                    work_date,
                    hours
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    work_record.employee_id,
                    work_record.project_id,
                    work_record.work_date.isoformat(),
                    work_record.hours,
                ),
            )
        if cursor.lastrowid is None:
            raise sqlite3.DatabaseError(
                "No se obtuvo el identificador del registro de trabajo."
            )
        return cursor.lastrowid
