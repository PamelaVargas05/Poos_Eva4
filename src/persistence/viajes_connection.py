"""Conexiones MySQL independientes para Viajes Aventura."""

import os
from pathlib import Path

import mysql.connector
from mysql.connector.connection import MySQLConnection
from dotenv import load_dotenv

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3307
DATABASE_NAME = "viajes_aventura"
USER_ENVIRONMENT_VARIABLE = "VIAJES_DB_USER"
PASSWORD_ENVIRONMENT_VARIABLE = "VIAJES_DB_PASSWORD"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _read_credentials() -> tuple[str, str]:
    missing_variables = [
        variable
        for variable in (USER_ENVIRONMENT_VARIABLE, PASSWORD_ENVIRONMENT_VARIABLE)
        if variable not in os.environ
    ]
    if missing_variables:
        missing = ", ".join(missing_variables)
        raise RuntimeError(
            f"Configura las variables de entorno requeridas: {missing}."
        )

    username = os.environ[USER_ENVIRONMENT_VARIABLE]
    password = os.environ[PASSWORD_ENVIRONMENT_VARIABLE]
    if not username.strip():
        raise RuntimeError(
            f"La variable {USER_ENVIRONMENT_VARIABLE} no puede estar vacía."
        )
    return username, password


def _open_connection(database: str | None) -> MySQLConnection:
    username, password = _read_credentials()
    options: dict[str, str | int] = {
        "host": MYSQL_HOST,
        "port": MYSQL_PORT,
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "user": username,
        "password": password,
        "connection_timeout": 10,
    }
    if database is not None:
        options["database"] = database

    try:
        return mysql.connector.connect(**options)
    except mysql.connector.Error as error:
        error_code = (
            f" (error MySQL {error.errno})" if error.errno is not None else ""
        )
        raise ConnectionError(
            f"No se pudo conectar con MySQL en {MYSQL_HOST}:{MYSQL_PORT}"
            f"{error_code}."
        ) from error


def get_connection() -> MySQLConnection:
    return _open_connection(DATABASE_NAME)


def get_server_connection() -> MySQLConnection:
    return _open_connection(None)
