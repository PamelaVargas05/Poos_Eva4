"""Esquema idempotente para los datos turísticos."""

from contextlib import closing
from typing import Callable

import mysql.connector
from mysql.connector.connection import MySQLConnection

from src.persistence.viajes_connection import get_connection

CREATE_TABLES_SQL = (
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        full_name VARCHAR(120) NOT NULL,
        email VARCHAR(254) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'customer',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id),
        CONSTRAINT uq_users_email UNIQUE (email),
        CONSTRAINT chk_users_role CHECK (role IN ('customer', 'admin')),
        CONSTRAINT chk_users_name CHECK (CHAR_LENGTH(TRIM(full_name)) > 0)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS destinations (
        destination_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(120) NOT NULL,
        country VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        PRIMARY KEY (destination_id),
        CONSTRAINT uq_destinations_name_country UNIQUE (name, country),
        CONSTRAINT chk_destinations_name CHECK (CHAR_LENGTH(TRIM(name)) > 0),
        CONSTRAINT chk_destinations_country CHECK (CHAR_LENGTH(TRIM(country)) > 0)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS travel_packages (
        package_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(160) NOT NULL,
        description TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        unit_price DECIMAL(12, 2) NOT NULL,
        available_slots INT UNSIGNED NOT NULL,
        PRIMARY KEY (package_id),
        CONSTRAINT chk_packages_name CHECK (CHAR_LENGTH(TRIM(name)) > 0),
        CONSTRAINT chk_packages_dates CHECK (end_date >= start_date),
        CONSTRAINT chk_packages_price CHECK (unit_price > 0),
        CONSTRAINT chk_packages_slots CHECK (available_slots >= 0)
    ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS package_destinations (
        package_id BIGINT UNSIGNED NOT NULL,
        destination_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (package_id, destination_id),
        CONSTRAINT fk_package_destinations_package
            FOREIGN KEY (package_id) REFERENCES travel_packages (package_id)
            ON DELETE CASCADE,
        CONSTRAINT fk_package_destinations_destination
            FOREIGN KEY (destination_id) REFERENCES destinations (destination_id)
            ON DELETE RESTRICT
    ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        package_id BIGINT UNSIGNED NOT NULL,
        booked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        travelers INT UNSIGNED NOT NULL,
        unit_price DECIMAL(12, 2) NOT NULL,
        total_price DECIMAL(14, 2) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
        PRIMARY KEY (reservation_id),
        KEY ix_reservations_user (user_id),
        KEY ix_reservations_package_status (package_id, status),
        CONSTRAINT fk_reservations_user
            FOREIGN KEY (user_id) REFERENCES users (user_id)
            ON DELETE RESTRICT,
        CONSTRAINT fk_reservations_package
            FOREIGN KEY (package_id) REFERENCES travel_packages (package_id)
            ON DELETE RESTRICT,
        CONSTRAINT chk_reservations_travelers CHECK (travelers > 0),
        CONSTRAINT chk_reservations_prices
            CHECK (unit_price > 0 AND total_price > 0),
        CONSTRAINT chk_reservations_status
            CHECK (status IN ('confirmed', 'cancelled'))
    ) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4
      COLLATE utf8mb4_unicode_ci
    """,
)
TABLE_NAMES = (
    "users",
    "destinations",
    "travel_packages",
    "package_destinations",
    "reservations",
)


def initialize_tables(
    connection_factory: Callable[[], MySQLConnection] = get_connection,
) -> None:
    with closing(connection_factory()) as connection:
        with closing(connection.cursor()) as cursor:
            for statement in CREATE_TABLES_SQL:
                cursor.execute(statement)


def verify_tables(
    connection_factory: Callable[[], MySQLConnection] = get_connection,
) -> None:
    placeholders = ", ".join(["%s"] * len(TABLE_NAMES))
    with closing(connection_factory()) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = DATABASE() "
                f"AND table_name IN ({placeholders})",
                TABLE_NAMES,
            )
            result = cursor.fetchone()
    if result is None or int(result[0]) != len(TABLE_NAMES):
        raise RuntimeError(
            "Falta inicializar el esquema de Viajes Aventura con "
            "`python -m src.viajes.persistence.schema`."
        )


def main() -> int:
    try:
        initialize_tables()
    except (ConnectionError, RuntimeError, mysql.connector.Error):
        print(
            "No se pudo inicializar el esquema. Verifique la conexión "
            "y el permiso CREATE de la cuenta MariaDB."
        )
        return 1
    print("Esquema de Viajes Aventura preparado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

