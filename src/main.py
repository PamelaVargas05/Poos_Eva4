"""Demostración inicial de EcoTech Solutions con SQLite."""

import sqlite3
from contextlib import closing
from datetime import date

from domain.department import Department
from domain.employee import Employee
from domain.project import Project
from domain.work_record import WorkRecord
from persistence.connection import create_connection
from persistence.create_db import create_tables
from persistence.department_dao import DepartmentDAO
from persistence.employee_dao import EmployeeDAO
from persistence.project_dao import ProjectDAO
from persistence.work_record_dao import WorkRecordDAO


def main() -> int:
    print("EcoTech Solutions - demostración de persistencia")
    try:
        with closing(create_connection()) as connection:
            create_tables(connection)

            department = Department(name="Departamento de prueba")
            department_id = DepartmentDAO(connection).insert(department)
            department.assign_department_id(department_id)

            employee = Employee(
                name="Empleado de prueba",
                department_id=department_id,
            )
            employee_id = EmployeeDAO(connection).insert(employee)
            employee.assign_employee_id(employee_id)
            department.add_employee(employee)

            project = Project(name="Proyecto de prueba")
            project_id = ProjectDAO(connection).insert(project)
            project.assign_project_id(project_id)

            work_record = WorkRecord(
                employee_id=employee_id,
                project_id=project_id,
                work_date=date.today(),
                hours=7.5,
            )
            work_record_id = WorkRecordDAO(connection).insert(work_record)
            work_record.assign_work_record_id(work_record_id)
            employee.add_work_record(work_record)
            project.add_work_record(work_record)
    except sqlite3.Error:
        print("No se pudo completar la demostración de la base de datos.")
        return 1
    except ValueError as error:
        print(f"No se pudo validar un dato de prueba: {error}")
        return 1

    print(f"Departamento insertado (ID {department_id}).")
    print(f"Proyecto insertado (ID {project_id}).")
    print(f"Empleado asociado insertado (ID {employee_id}).")
    print(f"Registro de trabajo insertado (ID {work_record_id}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
