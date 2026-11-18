"""Pruebas unitarias simuladas para la persistencia MySQL de Viajes Aventura."""

import os
import unittest
from unittest.mock import Mock, patch

import mysql.connector

from src.persistence import viajes_connection
from src.persistence.create_viajes_db import (
    CREATE_DATABASE_SQL,
    initialize_database,
)
from src.persistence.viajes_connection import get_connection, get_server_connection


class ViajesConnectionTests(unittest.TestCase):
    def test_get_connection_uses_mysql_options_and_environment_credentials(
        self,
    ) -> None:
        connection = Mock()
        credentials = {
            viajes_connection.USER_ENVIRONMENT_VARIABLE: "unit-test-user",
            viajes_connection.PASSWORD_ENVIRONMENT_VARIABLE: "unit-test-password",
        }
        with patch.dict(os.environ, credentials, clear=True):
            with patch.object(
                viajes_connection.mysql.connector,
                "connect",
                return_value=connection,
            ) as connect:
                result = get_connection()

        self.assertIs(result, connection)
        connect.assert_called_once_with(
            host="127.0.0.1",
            port=3307,
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
            user="unit-test-user",
            password="unit-test-password",
            connection_timeout=10,
            database="viajes_aventura",
        )

    def test_missing_credentials_are_reported_without_connecting(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(
                viajes_connection.mysql.connector, "connect"
            ) as connect:
                with self.assertRaisesRegex(
                    RuntimeError, "VIAJES_DB_USER, VIAJES_DB_PASSWORD"
                ):
                    get_connection()

        connect.assert_not_called()

    def test_server_connection_omits_database_name(self) -> None:
        connection = Mock()
        credentials = {
            viajes_connection.USER_ENVIRONMENT_VARIABLE: "unit-test-user",
            viajes_connection.PASSWORD_ENVIRONMENT_VARIABLE: "unit-test-password",
        }
        with patch.dict(os.environ, credentials, clear=True):
            with patch.object(
                viajes_connection.mysql.connector,
                "connect",
                return_value=connection,
            ) as connect:
                self.assertIs(get_server_connection(), connection)

        self.assertNotIn("database", connect.call_args.kwargs)

    def test_connection_errors_are_reported_without_credentials(self) -> None:
        credentials = {
            viajes_connection.USER_ENVIRONMENT_VARIABLE: "unit-test-user",
            viajes_connection.PASSWORD_ENVIRONMENT_VARIABLE: "secret-for-test",
        }
        with patch.dict(os.environ, credentials, clear=True):
            with patch.object(
                viajes_connection.mysql.connector,
                "connect",
                side_effect=mysql.connector.Error(
                    errno=1045, msg="Access denied"
                ),
            ):
                with self.assertRaises(ConnectionError) as raised:
                    get_connection()

        self.assertNotIn("secret-for-test", str(raised.exception))
        self.assertIn("1045", str(raised.exception))


class ViajesDatabaseInitializerTests(unittest.TestCase):
    def test_initializer_creates_database_without_creating_tables(self) -> None:
        connection = Mock()
        cursor = Mock()
        connection.cursor.return_value = cursor

        with patch(
            "src.persistence.create_viajes_db.get_server_connection",
            return_value=connection,
        ):
            initialize_database()

        cursor.execute.assert_called_once_with(CREATE_DATABASE_SQL)
        self.assertIn("CREATE DATABASE IF NOT EXISTS", CREATE_DATABASE_SQL)
        self.assertIn(
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
            CREATE_DATABASE_SQL,
        )
        self.assertNotIn("CREATE TABLE", CREATE_DATABASE_SQL)
        cursor.close.assert_called_once_with()
        connection.close.assert_called_once_with()

    def test_initializer_closes_resources_when_creation_fails(self) -> None:
        connection = Mock()
        cursor = Mock()
        cursor.execute.side_effect = mysql.connector.Error("permiso insuficiente")
        connection.cursor.return_value = cursor

        with patch(
            "src.persistence.create_viajes_db.get_server_connection",
            return_value=connection,
        ):
            with self.assertRaises(mysql.connector.Error):
                initialize_database()

        cursor.close.assert_called_once_with()
        connection.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
