"""Errores de aplicación con mensajes seguros para la interfaz."""


class NotFoundError(LookupError):
    """El registro solicitado no existe."""


class DuplicateRecordError(ValueError):
    """El registro viola una restricción de unicidad."""


class AvailabilityError(ValueError):
    """La disponibilidad no alcanza para la operación."""


class AuthenticationError(ValueError):
    """Credenciales no válidas."""
