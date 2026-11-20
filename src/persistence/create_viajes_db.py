"""Creación de la base MySQL sin crear tablas."""

from contextlib import closing

import mysql.connector

from .viajes_connection import DATABASE_NAME, get_server_connection


CREATE_DATABASE_SQL = (
    f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` "
    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
)


def initialize_database() -> None:
    with closing(get_server_connection()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(CREATE_DATABASE_SQL)


def main() -> int:
    try:
        initialize_database()
    except (ConnectionError, RuntimeError, mysql.connector.Error) as error:
        print(f"No se pudo inicializar la base de datos: {error}")
        return 1

    print(
        f"Base de datos MySQL '{DATABASE_NAME}' preparada. "
        "No se crearon tablas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
