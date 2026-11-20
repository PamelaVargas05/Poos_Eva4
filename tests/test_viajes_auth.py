import unittest
from unittest.mock import patch

from src.viajes import passwords
from src.viajes.auth import AuthenticationService, hash_password, verify_password
from src.viajes.domain import User
from src.viajes.errors import AuthenticationError


class FakeUserDAO:
    def __init__(self) -> None:
        self.users: dict[str, tuple[User, str]] = {}

    def create(self, user: User, password_hash: str) -> int:
        user.assign_id(1)
        self.users[user.email] = (user, password_hash)
        return 1

    def create_initial_admin(self, user: User, password_hash: str) -> int:
        return self.create(user, password_hash)

    def get_credentials_by_email(self, email: str) -> tuple[User, str] | None:
        return self.users.get(email.strip().lower())


class PasswordHashTests(unittest.TestCase):
    def test_password_hash_is_salted_and_verified_without_plaintext_storage(self) -> None:
        with patch.object(passwords, "_ITERATIONS", 100_000):
            first = hash_password("correct horse battery")
            second = hash_password("correct horse battery")
        self.assertNotEqual(first, second)
        self.assertNotIn("correct horse battery", first)
        self.assertTrue(verify_password("correct horse battery", first))
        self.assertFalse(verify_password("incorrect password", first))
        self.assertFalse(verify_password("anything", "invalid-format"))

    def test_password_policy_rejects_short_secrets(self) -> None:
        with self.assertRaisesRegex(ValueError, "10 y 1024"):
            hash_password("short")


class AuthenticationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.users = FakeUserDAO()
        with patch.object(passwords, "_ITERATIONS", 100_000):
            self.service = AuthenticationService(self.users)

    def test_register_login_logout_and_generic_invalid_credential_error(self) -> None:
        with patch.object(passwords, "_ITERATIONS", 100_000):
            user = self.service.register(
                "Pamela Vargas", "pamela@example.com", "secure password 1"
            )
        self.assertEqual(user.role, "customer")
        self.assertIsNone(self.service.current_user)

        logged_in = self.service.login("PAMELA@example.com", "secure password 1")
        self.assertIs(logged_in, user)
        with self.assertRaisesRegex(AuthenticationError, "Correo o contraseña"):
            self.service.login("pamela@example.com", "wrong password")
        with self.assertRaisesRegex(AuthenticationError, "Correo o contraseña"):
            self.service.login("unknown@example.com", "wrong password")
        self.service.logout()
        self.assertIsNone(self.service.current_user)

    def test_admin_role_is_required_for_restricted_actions(self) -> None:
        with self.assertRaises(PermissionError):
            self.service.require_role("admin")
        with patch.object(passwords, "_ITERATIONS", 100_000):
            admin = self.service.bootstrap_admin(
                "Admin User", "admin@example.com", "admin password 1"
            )
        self.assertIsNone(self.service.current_user)
        self.service.login("admin@example.com", "admin password 1")
        self.assertEqual(self.service.require_role("admin").user_id, admin.user_id)


if __name__ == "__main__":
    unittest.main()
