"""Utilidades pequeñas compartidas por los DAO turísticos."""

from contextlib import closing, contextmanager
from typing import Callable, Generator

from mysql.connector.cursor import MySQLCursor, MySQLCursorDict
from mysql.connector.connection import MySQLConnection


@contextmanager
def database_cursor(
    connection_factory: Callable[[], MySQLConnection],
    dictionary: bool = False,
) -> Generator[tuple[MySQLConnection, MySQLCursor | MySQLCursorDict], None, None]:
    with closing(connection_factory()) as connection:
        with closing(connection.cursor(dictionary=dictionary)) as cursor:
            yield connection, cursor


def rollback(connection: MySQLConnection) -> None:
    connection.rollback()
