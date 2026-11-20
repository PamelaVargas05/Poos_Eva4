import unittest
from unittest.mock import Mock

from src.viajes.persistence.schema import (
    CREATE_TABLES_SQL,
    initialize_tables,
    verify_tables,
)


class ViajesSchemaTests(unittest.TestCase):
    def test_creates_tourism_tables_idempotently_without_dropping_data(self) -> None:
        connection = Mock()
        cursor = Mock()
        connection.cursor.return_value = cursor

        initialize_tables(lambda: connection)

        self.assertEqual(len(CREATE_TABLES_SQL), 5)
        self.assertEqual(
            cursor.execute.call_args_list,
            [unittest.mock.call(statement) for statement in CREATE_TABLES_SQL],
        )
        self.assertTrue(
            all("CREATE TABLE IF NOT EXISTS" in statement for statement in CREATE_TABLES_SQL)
        )
        self.assertTrue(all("DROP " not in statement for statement in CREATE_TABLES_SQL))
        cursor.close.assert_called_once_with()
        connection.close.assert_called_once_with()

    def test_closes_connection_when_table_creation_fails(self) -> None:
        connection = Mock()
        cursor = Mock()
        cursor.execute.side_effect = RuntimeError("DDL rejected")
        connection.cursor.return_value = cursor

        with self.assertRaisesRegex(RuntimeError, "DDL rejected"):
            initialize_tables(lambda: connection)

        cursor.close.assert_called_once_with()
        connection.close.assert_called_once_with()

    def test_schema_check_is_read_only_and_requires_all_tables(self) -> None:
        connection = Mock()
        cursor = Mock()
        cursor.fetchone.return_value = (5,)
        connection.cursor.return_value = cursor

        verify_tables(lambda: connection)

        statement, parameters = cursor.execute.call_args.args
        self.assertIn("information_schema.tables", statement)
        self.assertEqual(parameters, (
            "users",
            "destinations",
            "travel_packages",
            "package_destinations",
            "reservations",
        ))
        self.assertNotIn("CREATE", statement)
        self.assertNotIn("DELETE", statement)

    def test_schema_check_reports_missing_tables(self) -> None:
        connection = Mock()
        cursor = Mock()
        cursor.fetchone.return_value = (4,)
        connection.cursor.return_value = cursor

        with self.assertRaisesRegex(RuntimeError, "Falta inicializar"):
            verify_tables(lambda: connection)


if __name__ == "__main__":
    unittest.main()
