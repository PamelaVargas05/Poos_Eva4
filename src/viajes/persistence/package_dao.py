"""CRUD transaccional de paquetes y sus destinos."""

from datetime import date
from typing import Callable

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict

from src.persistence.viajes_connection import get_connection
from src.viajes.domain import Destination, TravelPackage
from src.viajes.errors import NotFoundError
from ._common import database_cursor, rollback


class TravelPackageDAO:
    def __init__(
        self, connection_factory: Callable[[], MySQLConnection] = get_connection
    ) -> None:
        self._connection_factory = connection_factory

    @staticmethod
    def _destination_ids(cursor: MySQLCursorDict, package_id: int) -> tuple[int, ...]:
        cursor.execute(
            "SELECT destination_id FROM package_destinations "
            "WHERE package_id = %s ORDER BY destination_id",
            (package_id,),
        )
        return tuple(int(row["destination_id"]) for row in cursor.fetchall())

    @classmethod
    def _from_row(cls, cursor: MySQLCursorDict, row: dict[str, object]) -> TravelPackage:
        package_id = int(row["package_id"])
        start_date = row["start_date"]
        end_date = row["end_date"]
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise RuntimeError("La base de datos devolvió fechas de paquete inválidas.")
        return TravelPackage(
            name=str(row["name"]),
            description=str(row["description"]),
            start_date=start_date,
            end_date=end_date,
            unit_price=str(row["unit_price"]),
            available_slots=int(row["available_slots"]),
            destination_ids=cls._destination_ids(cursor, package_id),
            package_id=package_id,
        )

    @staticmethod
    def _validate_destinations(
        cursor: MySQLCursorDict, destination_ids: tuple[int, ...]
    ) -> None:
        placeholders = ", ".join(["%s"] * len(destination_ids))
        cursor.execute(
            f"SELECT destination_id FROM destinations "
            f"WHERE destination_id IN ({placeholders})",
            destination_ids,
        )
        found = {int(row["destination_id"]) for row in cursor.fetchall()}
        if found != set(destination_ids):
            raise NotFoundError("Uno o más destinos del paquete no existen.")

    def create(self, package: TravelPackage) -> int:
        if package.package_id is not None:
            raise ValueError("Solo se pueden registrar paquetes sin identificador.")
        if package.available_slots <= 0:
            raise ValueError("Un paquete nuevo debe tener disponibilidad positiva.")
        with database_cursor(self._connection_factory, dictionary=True) as (
            connection,
            cursor,
        ):
            try:
                connection.start_transaction()
                self._validate_destinations(cursor, package.destination_ids)
                cursor.execute(
                    "INSERT INTO travel_packages "
                    "(name, description, start_date, end_date, unit_price, available_slots) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        package.name,
                        package.description,
                        package.start_date,
                        package.end_date,
                        package.unit_price,
                        package.available_slots,
                    ),
                )
                package_id = int(cursor.lastrowid)
                cursor.executemany(
                    "INSERT INTO package_destinations (package_id, destination_id) "
                    "VALUES (%s, %s)",
                    [(package_id, item) for item in package.destination_ids],
                )
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise ValueError(
                    "No se pudo guardar el paquete por una relación inválida."
                ) from error
            except Exception:
                rollback(connection)
                raise
        package.assign_id(package_id)
        return package_id

    def get_by_id(self, package_id: int) -> TravelPackage:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT package_id, name, description, start_date, end_date, "
                "unit_price, available_slots FROM travel_packages WHERE package_id = %s",
                (package_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise NotFoundError("No se encontró el paquete solicitado.")
            return self._from_row(cursor, row)

    def list_all(self) -> list[TravelPackage]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT package_id, name, description, start_date, end_date, "
                "unit_price, available_slots FROM travel_packages "
                "ORDER BY start_date, name"
            )
            return [self._from_row(cursor, row) for row in cursor.fetchall()]

    def get_destinations(self, package_id: int) -> list[Destination]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT package_id FROM travel_packages WHERE package_id = %s",
                (package_id,),
            )
            if cursor.fetchone() is None:
                raise NotFoundError("No se encontró el paquete solicitado.")
            cursor.execute(
                "SELECT d.destination_id, d.name, d.country, d.description "
                "FROM destinations AS d JOIN package_destinations AS pd "
                "ON pd.destination_id = d.destination_id "
                "WHERE pd.package_id = %s ORDER BY d.name, d.country",
                (package_id,),
            )
            return [
                Destination(
                    name=str(row["name"]),
                    country=str(row["country"]),
                    description=str(row["description"]),
                    destination_id=int(row["destination_id"]),
                )
                for row in cursor.fetchall()
            ]

    def update(self, package_id: int, package: TravelPackage) -> None:
        with database_cursor(self._connection_factory, dictionary=True) as (
            connection,
            cursor,
        ):
            try:
                connection.start_transaction()
                cursor.execute(
                    "SELECT package_id FROM travel_packages WHERE package_id = %s "
                    "FOR UPDATE",
                    (package_id,),
                )
                if cursor.fetchone() is None:
                    raise NotFoundError("No se encontró el paquete solicitado.")
                self._validate_destinations(cursor, package.destination_ids)
                cursor.execute(
                    "UPDATE travel_packages SET name = %s, description = %s, "
                    "start_date = %s, end_date = %s, unit_price = %s, "
                    "available_slots = %s WHERE package_id = %s",
                    (
                        package.name,
                        package.description,
                        package.start_date,
                        package.end_date,
                        package.unit_price,
                        package.available_slots,
                        package_id,
                    ),
                )
                cursor.execute(
                    "DELETE FROM package_destinations WHERE package_id = %s",
                    (package_id,),
                )
                cursor.executemany(
                    "INSERT INTO package_destinations (package_id, destination_id) "
                    "VALUES (%s, %s)",
                    [(package_id, item) for item in package.destination_ids],
                )
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise ValueError(
                    "No se pudo modificar el paquete por una relación inválida."
                ) from error
            except Exception:
                rollback(connection)
                raise

    def delete(self, package_id: int) -> None:
        with database_cursor(self._connection_factory) as (connection, cursor):
            try:
                cursor.execute(
                    "DELETE FROM travel_packages WHERE package_id = %s",
                    (package_id,),
                )
                if cursor.rowcount == 0:
                    raise NotFoundError("No se encontró el paquete solicitado.")
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise ValueError(
                    "No se puede eliminar un paquete con reservas asociadas."
                ) from error
            except Exception:
                rollback(connection)
                raise
