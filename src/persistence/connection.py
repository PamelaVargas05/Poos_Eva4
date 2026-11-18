"""Creación centralizada de conexiones SQLite."""

import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "ecotech.db"
)


def create_connection(
    database_path: str | Path | None = None,
) -> sqlite3.Connection:
    if database_path is None:
        location = DEFAULT_DATABASE_PATH
    elif str(database_path) == ":memory:":
        location = ":memory:"
    else:
        location = Path(database_path)

    if location != ":memory:":
        Path(location).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(location))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
