"""Operaciones CRUD de destinos."""

from typing import Callable

import mysql.connector
from mysql.connector.connection import MySQLConnection

from src.persistence.viajes_connection import get_connection
from src.viajes.domain import Destination
from src.viajes.errors import DuplicateRecordError, NotFoundError
from ._common import database_cursor, rollback


class DestinationDAO:
    def __init__(
        self, connection_factory: Callable[[], MySQLConnection] = get_connection
    ) -> None:
        self._connection_factory = connection_factory

    @staticmethod
    def _from_row(row: dict[str, object]) -> Destination:
        return Destination(
            name=str(row["name"]),
            country=str(row["country"]),
            description=str(row["description"]),
            destination_id=int(row["destination_id"]),
        )

    def create(self, destination: Destination) -> int:
        if destination.destination_id is not None:
            raise ValueError("Solo se pueden registrar destinos sin identificador.")
        with database_cursor(self._connection_factory) as (connection, cursor):
            try:
                connection.start_transaction()
                cursor.execute(
                    "INSERT INTO destinations (name, country, description) "
                    "VALUES (%s, %s, %s)",
                    (destination.name, destination.country, destination.description),
                )
                destination_id = int(cursor.lastrowid)
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise DuplicateRecordError(
                    "Ya existe un destino con ese nombre y país."
                ) from error
        destination.assign_id(destination_id)
        return destination_id

    def get_by_id(self, destination_id: int) -> Destination:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT destination_id, name, country, description "
                "FROM destinations WHERE destination_id = %s",
                (destination_id,),
            )
            row = cursor.fetchone()
        if row is None:
            raise NotFoundError("No se encontró el destino solicitado.")
        return self._from_row(row)

    def list_all(self) -> list[Destination]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT destination_id, name, country, description "
                "FROM destinations ORDER BY name, country"
            )
            return [self._from_row(row) for row in cursor.fetchall()]

    def update(self, destination_id: int, destination: Destination) -> None:
        with database_cursor(self._connection_factory) as (connection, cursor):
            try:
                connection.start_transaction()
                cursor.execute(
                    "UPDATE destinations SET name = %s, country = %s, description = %s "
                    "WHERE destination_id = %s",
                    (
                        destination.name,
                        destination.country,
                        destination.description,
                        destination_id,
                    ),
                )
                if cursor.rowcount == 0:
                    cursor.execute(
                        "SELECT 1 FROM destinations WHERE destination_id = %s",
                        (destination_id,),
                    )
                    if cursor.fetchone() is None:
                        raise NotFoundError("No se encontró el destino solicitado.")
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise DuplicateRecordError(
                    "Ya existe un destino con ese nombre y país."
                ) from error
            except Exception:
                rollback(connection)
                raise

    def delete(self, destination_id: int) -> None:
        with database_cursor(self._connection_factory) as (connection, cursor):
            try:
                connection.start_transaction()
                cursor.execute(
                    "DELETE FROM destinations WHERE destination_id = %s",
                    (destination_id,),
                )
                if cursor.rowcount == 0:
                    raise NotFoundError("No se encontró el destino solicitado.")
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise ValueError(
                    "No se puede eliminar un destino asociado a paquetes."
                ) from error
            except Exception:
                rollback(connection)
                raise
