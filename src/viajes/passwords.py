"""Hash y verificación de contraseñas con la biblioteca estándar."""

import hashlib
import hmac
import secrets

_HASH_NAME = "sha256"
_ITERATIONS = 600_000
_MIN_ITERATIONS = 100_000
_MAX_ITERATIONS = 2_000_000
_SALT_BYTES = 16
_KEY_BYTES = 32
_MAX_PASSWORD_LENGTH = 1024


def _validate_password(password: str) -> None:
    if not isinstance(password, str) or not 10 <= len(password) <= _MAX_PASSWORD_LENGTH:
        raise ValueError("La contraseña debe tener entre 10 y 1024 caracteres.")


def _parse_hash(stored_hash: str) -> tuple[int, bytes, bytes] | None:
    if not isinstance(stored_hash, str):
        return None
    try:
        algorithm, iteration_text, salt_text, digest_text = stored_hash.split("$")
        iterations = int(iteration_text)
        salt = bytes.fromhex(salt_text)
        digest = bytes.fromhex(digest_text)
    except (ValueError, TypeError):
        return None
    if (
        algorithm != "pbkdf2_sha256"
        or not _MIN_ITERATIONS <= iterations <= _MAX_ITERATIONS
        or len(salt) != _SALT_BYTES
        or len(digest) != _KEY_BYTES
    ):
        return None
    return iterations, salt, digest


def is_password_hash(stored_hash: str) -> bool:
    return _parse_hash(stored_hash) is not None


def hash_password(password: str) -> str:
    _validate_password(password)
    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        _HASH_NAME, password.encode("utf-8"), salt, _ITERATIONS, dklen=_KEY_BYTES
    )
    return f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    if not isinstance(password, str) or len(password) > _MAX_PASSWORD_LENGTH:
        return False
    parsed_hash = _parse_hash(stored_hash)
    if parsed_hash is None:
        return False
    iterations, salt, expected = parsed_hash
    try:
        candidate = password.encode("utf-8")
    except UnicodeEncodeError:
        return False
    actual = hashlib.pbkdf2_hmac(
        _HASH_NAME, candidate, salt, iterations, dklen=_KEY_BYTES
    )
    return hmac.compare_digest(actual, expected)
