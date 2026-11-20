"""Registro y consulta de usuarios."""

from typing import Callable

import mysql.connector
from mysql.connector.connection import MySQLConnection

from src.persistence.viajes_connection import get_connection
from src.viajes.domain import User
from src.viajes.errors import DuplicateRecordError, NotFoundError
from src.viajes.passwords import is_password_hash
from ._common import database_cursor, rollback


class UserDAO:
    def __init__(
        self, connection_factory: Callable[[], MySQLConnection] = get_connection
    ) -> None:
        self._connection_factory = connection_factory

    @staticmethod
    def _from_row(row: dict[str, object]) -> User:
        return User(
            full_name=str(row["full_name"]),
            email=str(row["email"]),
            role=str(row["role"]),
            user_id=int(row["user_id"]),
        )

    def create(self, user: User, password_hash: str) -> int:
        if user.role != "customer":
            raise ValueError("El registro público solo permite crear clientes.")
        if user.user_id is not None:
            raise ValueError("Solo se pueden registrar usuarios sin identificador.")
        if not is_password_hash(password_hash):
            raise ValueError("La credencial segura es obligatoria.")
        with database_cursor(self._connection_factory) as (connection, cursor):
            try:
                connection.start_transaction()
                cursor.execute(
                    "INSERT INTO users (full_name, email, password_hash, role) "
                    "VALUES (%s, %s, %s, 'customer')",
                    (user.full_name, user.email, password_hash),
                )
                user_id = int(cursor.lastrowid)
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise DuplicateRecordError(
                    "Ya existe una cuenta con ese correo electrónico."
                ) from error
        user.assign_id(user_id)
        return user_id

    def create_initial_admin(self, user: User, password_hash: str) -> int:
        if user.role != "admin":
            raise ValueError("La cuenta inicial debe tener rol administrador.")
        if user.user_id is not None:
            raise ValueError("Solo se pueden registrar usuarios sin identificador.")
        if not is_password_hash(password_hash):
            raise ValueError("La credencial segura es obligatoria.")
        with database_cursor(self._connection_factory, dictionary=True) as (
            connection,
            cursor,
        ):
            lock_acquired = False
            try:
                cursor.execute(
                    "SELECT GET_LOCK(%s, %s) AS acquired",
                    ("viajes_aventura_admin_bootstrap", 10),
                )
                lock = cursor.fetchone()
                if lock is None or lock["acquired"] != 1:
                    raise RuntimeError(
                        "No se pudo obtener el bloqueo para crear el administrador."
                    )
                lock_acquired = True
                connection.start_transaction()
                cursor.execute("SELECT user_id FROM users WHERE role = 'admin' LIMIT 1")
                if cursor.fetchone() is not None:
                    raise ValueError("Ya existe una cuenta administradora.")
                cursor.execute(
                    "INSERT INTO users (full_name, email, password_hash, role) "
                    "VALUES (%s, %s, %s, 'admin')",
                    (user.full_name, user.email, password_hash),
                )
                user_id = int(cursor.lastrowid)
                connection.commit()
            except mysql.connector.IntegrityError as error:
                rollback(connection)
                raise DuplicateRecordError(
                    "Ya existe una cuenta con ese correo electrónico."
                ) from error
            except Exception:
                rollback(connection)
                raise
            finally:
                if lock_acquired:
                    cursor.execute(
                        "SELECT RELEASE_LOCK(%s)",
                        ("viajes_aventura_admin_bootstrap",),
                    )
                    cursor.fetchone()
        user.assign_id(user_id)
        return user_id

    def get_by_id(self, user_id: int) -> User:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT user_id, full_name, email, role FROM users WHERE user_id = %s",
                (user_id,),
            )
            row = cursor.fetchone()
        if row is None:
            raise NotFoundError("No se encontró el usuario solicitado.")
        return self._from_row(row)

    def get_credentials_by_email(self, email: str) -> tuple[User, str] | None:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT user_id, full_name, email, role, password_hash "
                "FROM users WHERE email = %s",
                (email.strip().lower(),),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return self._from_row(row), str(row["password_hash"])

    def find_by_email(self, email: str) -> User | None:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT user_id, full_name, email, role FROM users WHERE email = %s",
                (email.strip().lower(),),
            )
            row = cursor.fetchone()
        return self._from_row(row) if row is not None else None

    def list_all(self) -> list[User]:
        with database_cursor(self._connection_factory, dictionary=True) as (_, cursor):
            cursor.execute(
                "SELECT user_id, full_name, email, role FROM users ORDER BY full_name"
            )
            return [self._from_row(row) for row in cursor.fetchall()]
