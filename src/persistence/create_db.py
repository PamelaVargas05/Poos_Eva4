"""Creación del esquema SQLite inicial."""

import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS work_records (
    work_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    work_date TEXT NOT NULL,
    hours REAL NOT NULL CHECK (hours > 0),
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
);
"""


def create_tables(connection: sqlite3.Connection) -> None:
    with connection:
        connection.executescript(SCHEMA)
