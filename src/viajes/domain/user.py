"""Cuenta de usuario sin exposición de contraseñas en texto plano."""

from ._validation import positive_id, required_text


class User:
    __slots__ = ("__user_id", "__full_name", "__email", "__role")

    def __init__(
        self,
        full_name: str,
        email: str,
        role: str = "customer",
        user_id: int | None = None,
    ) -> None:
        self.__user_id = positive_id(user_id, "El usuario") if user_id is not None else None
        self.__full_name = required_text(full_name, "El nombre", 120)
        normalized_email = required_text(email, "El correo", 254).lower()
        if (
            "@" not in normalized_email
            or normalized_email.startswith("@")
            or normalized_email.endswith("@")
            or "." not in normalized_email.rsplit("@", 1)[1]
        ):
            raise ValueError("El correo electrónico no es válido.")
        self.__email = normalized_email
        if not isinstance(role, str) or role not in {"customer", "admin"}:
            raise ValueError("El rol indicado no es válido.")
        self.__role = role

    @property
    def user_id(self) -> int | None:
        return self.__user_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def role(self) -> str:
        return self.__role

    def assign_id(self, user_id: int) -> None:
        if self.__user_id is not None:
            raise ValueError("El usuario ya tiene identificador.")
        self.__user_id = positive_id(user_id, "El usuario")
