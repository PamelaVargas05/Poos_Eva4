"""Cálculo centralizado de precios de paquetes y reservas."""

from decimal import Decimal, InvalidOperation

from ._validation import positive_decimal

MAX_TRAVELERS = 4_294_967_295
MAX_TOTAL_PRICE = Decimal("999999999999.99")


def calculate_total_price(
    unit_price: Decimal | int | float | str, travelers: int
) -> Decimal:
    if (
        isinstance(travelers, bool)
        or not isinstance(travelers, int)
        or not 1 <= travelers <= MAX_TRAVELERS
    ):
        raise ValueError("La cantidad de viajeros está fuera del rango permitido.")
    amount = positive_decimal(unit_price, "El precio unitario")
    try:
        total = (amount * travelers).quantize(Decimal("0.01"))
    except InvalidOperation:
        raise ValueError("El costo total excede el rango monetario permitido.") from None
    if total > MAX_TOTAL_PRICE:
        raise ValueError("El costo total excede el rango monetario permitido.")
    return total
