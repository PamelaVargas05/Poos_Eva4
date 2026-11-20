"""Registro, autenticación y sesión local para la interfaz de consola."""

from src.viajes.domain import User
from src.viajes.errors import AuthenticationError
from src.viajes.passwords import hash_password, verify_password
from src.viajes.persistence.user_dao import UserDAO

class AuthenticationService:
    def __init__(self, users: UserDAO | None = None) -> None:
        self._users = users or UserDAO()
        self._current_user: User | None = None
        self._dummy_hash = hash_password("this-is-not-a-user-password")

    @property
    def current_user(self) -> User | None:
        return self._current_user

    def register(self, full_name: str, email: str, password: str) -> User:
        user = User(full_name, email)
        stored_hash = hash_password(password)
        self._users.create(user, stored_hash)
        return user

    def bootstrap_admin(self, full_name: str, email: str, password: str) -> User:
        user = User(full_name, email, role="admin")
        stored_hash = hash_password(password)
        self._users.create_initial_admin(user, stored_hash)
        return user

    def login(self, email: str, password: str) -> User:
        if not isinstance(email, str) or not isinstance(password, str):
            raise AuthenticationError("Correo o contraseña incorrectos.")
        credentials = self._users.get_credentials_by_email(email)
        stored_hash = credentials[1] if credentials is not None else self._dummy_hash
        valid = verify_password(password, stored_hash)
        if credentials is None or not valid:
            raise AuthenticationError("Correo o contraseña incorrectos.")
        self._current_user = credentials[0]
        return self._current_user

    def logout(self) -> None:
        self._current_user = None

    def require_role(self, role: str) -> User:
        if self._current_user is None or self._current_user.role != role:
            raise PermissionError("No cuenta con permisos para esta operación.")
        return self._current_user
