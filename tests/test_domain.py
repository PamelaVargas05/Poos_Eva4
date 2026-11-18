"""Pruebas de validación de las entidades del dominio."""

import unittest
from datetime import date

from src.domain.department import Department
from src.domain.employee import Employee
from src.domain.project import Project
from src.domain.work_record import WorkRecord


class DomainTests(unittest.TestCase):
    def test_domain_objects_accept_valid_fictional_data(self) -> None:
        department = Department(name="Tecnología")
        project = Project(name="Eficiencia energética")
        employee = Employee(name="Alex Ejemplo", department_id=1)
        work_record = WorkRecord(
            employee_id=1,
            project_id=1,
            work_date=date(2026, 1, 15),
            hours=7.5,
        )

        self.assertEqual(department.name, "Tecnología")
        self.assertEqual(project.name, "Eficiencia energética")
        self.assertEqual(employee.department_id, 1)
        self.assertEqual(work_record.hours, 7.5)

    def test_domain_objects_reject_invalid_values(self) -> None:
        with self.assertRaises(ValueError):
            Department(name=" ")
        with self.assertRaises(ValueError):
            Employee(name="Empleado", department_id=0)
        with self.assertRaises(ValueError):
            WorkRecord(
                employee_id=1,
                project_id=1,
                work_date=date(2026, 1, 15),
                hours=0,
            )

    def test_domain_attributes_are_read_only_and_updates_are_validated(self) -> None:
        department = Department(name="Tecnología")
        with self.assertRaises(AttributeError):
            department.name = "Ventas"
        with self.assertRaises(ValueError):
            department.update_name(" ")
        department.update_name("Energía")
        self.assertEqual(department.name, "Energía")

        work_record = WorkRecord(
            employee_id=1,
            project_id=1,
            work_date=date(2026, 1, 15),
            hours=7.5,
        )
        with self.assertRaises(ValueError):
            work_record.update_hours(float("inf"))
        with self.assertRaises(ValueError):
            work_record.update_work_date("2026-01-15")
        work_record.update_hours(6)
        self.assertEqual(work_record.hours, 6.0)

    def test_related_objects_enforce_associations_and_return_snapshots(self) -> None:
        department = Department(name="Tecnología", department_id=1)
        employee = Employee(
            name="Alex Ejemplo", department_id=1, employee_id=2
        )
        project = Project(name="Eficiencia energética", project_id=3)
        work_record = WorkRecord(
            employee_id=2,
            project_id=3,
            work_date=date(2026, 1, 15),
            hours=7.5,
            work_record_id=4,
        )

        department.add_employee(employee)
        employee.add_work_record(work_record)
        project.add_work_record(work_record)
        self.assertEqual(department.get_employees(), (employee,))
        self.assertEqual(employee.get_work_records(), (work_record,))
        self.assertEqual(project.get_work_records(), (work_record,))
        with self.assertRaises(AttributeError):
            department.get_employees().append(employee)

        with self.assertRaises(ValueError):
            department.add_employee(Employee(name="Otra persona", department_id=5))
        with self.assertRaises(ValueError):
            employee.add_work_record(
                WorkRecord(
                    employee_id=9,
                    project_id=3,
                    work_date=date(2026, 1, 15),
                    hours=1,
                )
            )
        with self.assertRaises(ValueError):
            project.add_work_record(
                WorkRecord(
                    employee_id=2,
                    project_id=9,
                    work_date=date(2026, 1, 15),
                    hours=1,
                )
            )
        with self.assertRaises(ValueError):
            department.add_employee(employee)

    def test_department_can_have_multiple_employees(self) -> None:
        department = Department(name="Tecnología", department_id=1)
        first_employee = Employee(
            name="Alex Ejemplo", department_id=1, employee_id=2
        )
        second_employee = Employee(
            name="Sam Ejemplo", department_id=1, employee_id=3
        )

        department.add_employee(first_employee)
        department.add_employee(second_employee)

        self.assertEqual(
            department.get_employees(),
            (first_employee, second_employee),
        )

    def test_employee_can_have_multiple_work_records(self) -> None:
        employee = Employee(
            name="Alex Ejemplo", department_id=1, employee_id=2
        )
        first_record = WorkRecord(
            employee_id=2,
            project_id=3,
            work_date=date(2026, 1, 15),
            hours=7.5,
            work_record_id=4,
        )
        second_record = WorkRecord(
            employee_id=2,
            project_id=5,
            work_date=date(2026, 1, 16),
            hours=6,
            work_record_id=6,
        )

        employee.add_work_record(first_record)
        employee.add_work_record(second_record)

        self.assertEqual(
            employee.get_work_records(),
            (first_record, second_record),
        )

    def test_project_can_have_multiple_work_records(self) -> None:
        project = Project(name="Eficiencia energética", project_id=3)
        first_record = WorkRecord(
            employee_id=2,
            project_id=3,
            work_date=date(2026, 1, 15),
            hours=7.5,
            work_record_id=4,
        )
        second_record = WorkRecord(
            employee_id=5,
            project_id=3,
            work_date=date(2026, 1, 16),
            hours=6,
            work_record_id=6,
        )

        project.add_work_record(first_record)
        project.add_work_record(second_record)

        self.assertEqual(
            project.get_work_records(),
            (first_record, second_record),
        )

    def test_association_snapshots_reject_mutation_and_links_reject_duplicates(self) -> None:
        department = Department(name="Tecnología", department_id=1)
        employee = Employee(
            name="Alex Ejemplo", department_id=1, employee_id=2
        )
        project = Project(name="Eficiencia energética", project_id=3)
        work_record = WorkRecord(
            employee_id=2,
            project_id=3,
            work_date=date(2026, 1, 15),
            hours=7.5,
            work_record_id=4,
        )
        department.add_employee(employee)
        employee.add_work_record(work_record)
        project.add_work_record(work_record)

        employees = department.get_employees()
        employee_records = employee.get_work_records()
        project_records = project.get_work_records()
        with self.assertRaises(AttributeError):
            employees.append(Employee(name="Otra persona", department_id=1))
        with self.assertRaises(AttributeError):
            employee_records.append(work_record)
        with self.assertRaises(AttributeError):
            project_records.append(work_record)
        self.assertEqual(department.get_employees(), (employee,))
        self.assertEqual(employee.get_work_records(), (work_record,))
        self.assertEqual(project.get_work_records(), (work_record,))

        with self.assertRaises(ValueError):
            department.add_employee(
                Employee(
                    name="Alex duplicado",
                    department_id=1,
                    employee_id=2,
                )
            )
        with self.assertRaises(ValueError):
            employee.add_work_record(
                WorkRecord(
                    employee_id=2,
                    project_id=3,
                    work_date=date(2026, 1, 15),
                    hours=7.5,
                    work_record_id=4,
                )
            )
        with self.assertRaises(ValueError):
            project.add_work_record(
                WorkRecord(
                    employee_id=2,
                    project_id=3,
                    work_date=date(2026, 1, 15),
                    hours=7.5,
                    work_record_id=4,
                )
            )
        with self.assertRaises(ValueError):
            department.add_employee(
                Employee(name="Empleado ajeno", department_id=9)
            )
        with self.assertRaises(ValueError):
            employee.add_work_record(
                WorkRecord(
                    employee_id=9,
                    project_id=3,
                    work_date=date(2026, 1, 15),
                    hours=1,
                )
            )
        with self.assertRaises(ValueError):
            project.add_work_record(
                WorkRecord(
                    employee_id=2,
                    project_id=9,
                    work_date=date(2026, 1, 15),
                    hours=1,
                )
            )

    def test_generated_ids_can_only_be_assigned_once(self) -> None:
        department = Department(name="Tecnología")
        department.assign_department_id(1)
        self.assertEqual(department.department_id, 1)
        with self.assertRaises(ValueError):
            department.assign_department_id(2)


if __name__ == "__main__":
    unittest.main()
