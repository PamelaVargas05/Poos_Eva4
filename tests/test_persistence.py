"""Pruebas funcionales del esquema y los DAO con una base temporal."""

import sqlite3
import unittest
from datetime import date

from src.domain.department import Department
from src.domain.employee import Employee
from src.domain.project import Project
from src.domain.work_record import WorkRecord
from src.persistence.connection import create_connection
from src.persistence.create_db import create_tables
from src.persistence.department_dao import DepartmentDAO
from src.persistence.employee_dao import EmployeeDAO
from src.persistence.project_dao import ProjectDAO
from src.persistence.work_record_dao import WorkRecordDAO


class PersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = create_connection(":memory:")
        create_tables(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_creates_all_four_tables(self) -> None:
        rows = self.connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name IN (
                  'departments',
                  'employees',
                  'projects',
                  'work_records'
              )
            """
        ).fetchall()

        self.assertEqual(
            {row[0] for row in rows},
            {"departments", "employees", "projects", "work_records"},
        )

    def test_inserts_components_and_preserves_relationships(self) -> None:
        department_id = DepartmentDAO(self.connection).insert(
            Department(name="Departamento de prueba")
        )
        project_id = ProjectDAO(self.connection).insert(
            Project(name="Proyecto de prueba")
        )
        employee_id = EmployeeDAO(self.connection).insert(
            Employee(name="Empleado de prueba", department_id=department_id)
        )
        work_record_id = WorkRecordDAO(self.connection).insert(
            WorkRecord(
                employee_id=employee_id,
                project_id=project_id,
                work_date=date(2026, 1, 15),
                hours=7.5,
            )
        )

        record = self.connection.execute(
            """
            SELECT employee_id, project_id, work_date, hours
            FROM work_records
            WHERE work_record_id = ?
            """,
            (work_record_id,),
        ).fetchone()

        self.assertGreater(department_id, 0)
        self.assertGreater(project_id, 0)
        self.assertGreater(employee_id, 0)
        self.assertEqual(
            tuple(record),
            (employee_id, project_id, "2026-01-15", 7.5),
        )

    def test_foreign_keys_reject_missing_related_rows(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            EmployeeDAO(self.connection).insert(
                Employee(name="Sin departamento", department_id=999)
            )

        department_id = DepartmentDAO(self.connection).insert(
            Department(name="Departamento válido")
        )
        employee_id = EmployeeDAO(self.connection).insert(
            Employee(name="Empleado válido", department_id=department_id)
        )
        project_id = ProjectDAO(self.connection).insert(
            Project(name="Proyecto válido")
        )

        with self.assertRaises(sqlite3.IntegrityError):
            WorkRecordDAO(self.connection).insert(
                WorkRecord(
                    employee_id=999,
                    project_id=project_id,
                    work_date=date(2026, 1, 15),
                    hours=1.0,
                )
            )

        with self.assertRaises(sqlite3.IntegrityError):
            WorkRecordDAO(self.connection).insert(
                WorkRecord(
                    employee_id=employee_id,
                    project_id=999,
                    work_date=date(2026, 1, 15),
                    hours=1.0,
                )
            )


if __name__ == "__main__":
    unittest.main()
