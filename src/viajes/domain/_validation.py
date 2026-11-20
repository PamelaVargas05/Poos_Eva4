"""Validaciones compartidas por las entidades turísticas."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def required_text(value: str, field: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} debe ser texto.")
    cleaned = value.strip()
    if not cleaned or len(cleaned) > max_length:
        raise ValueError(f"{field} debe tener entre 1 y {max_length} caracteres.")
    return cleaned


def positive_id(value: int, field: str) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 0 < value <= 18_446_744_073_709_551_615
    ):
        raise ValueError(f"{field} debe ser un identificador positivo.")
    return value


def positive_decimal(value: Decimal | int | float | str, field: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{field} debe ser un monto positivo.")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field} debe ser un monto positivo.") from None
    if not amount.is_finite() or amount <= 0:
        raise ValueError(f"{field} debe ser un monto positivo.")
    try:
        normalized = amount.quantize(Decimal("0.01"))
    except InvalidOperation:
        raise ValueError(f"{field} excede el rango monetario permitido.") from None
    if normalized <= 0 or normalized > Decimal("9999999999.99"):
        raise ValueError(f"{field} excede el rango monetario permitido.")
    return normalized


def valid_date(value: date, field: str) -> date:
    if not isinstance(value, date) or isinstance(value, datetime):
        raise ValueError(f"{field} debe ser una fecha válida.")
    return value
