"""Interfaz de consola para la agencia Viajes Aventura."""

from datetime import date
from decimal import Decimal
from getpass import getpass
from typing import Callable

import mysql.connector

from src.viajes.auth import AuthenticationService
from src.viajes.domain import Destination, Reservation, TravelPackage
from src.viajes.persistence.destination_dao import DestinationDAO
from src.viajes.persistence.package_dao import TravelPackageDAO
from src.viajes.persistence.reservation_dao import ReservationDAO
from src.viajes.persistence.schema import initialize_tables, verify_tables
from src.viajes.persistence.user_dao import UserDAO


class ViajesConsole:
    def __init__(
        self,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
        password_reader: Callable[[str], str] = getpass,
    ) -> None:
        self._input = input_fn
        self._output = output_fn
        self._password = password_reader
        self._users = UserDAO()
        self._auth = AuthenticationService(self._users)
        self._destinations = DestinationDAO()
        self._packages = TravelPackageDAO()
        self._reservations = ReservationDAO()

    def bootstrap_admin(self) -> None:
        self._output("Creación única del administrador inicial.")
        name = self._input("Nombre: ")
        email = self._input("Correo: ")
        password = self._password("Contraseña (mínimo 10 caracteres): ")
        confirmation = self._password("Confirme la contraseña: ")
        if password != confirmation:
            raise ValueError("Las contraseñas no coinciden.")
        user = self._auth.bootstrap_admin(name, email, password)
        self._output(f"Administrador creado (ID {user.user_id}). Inicie sesión.")

    def run(self) -> int:
        verify_tables()
        self._output("Viajes Aventura")
        while True:
            user = self._auth.current_user
            if user is None:
                self._output("\n1) Iniciar sesión  2) Registrar usuario  0) Salir")
                choice = self._input("Opción: ").strip()
                if choice == "0":
                    return 0
                try:
                    if choice == "1":
                        self._login()
                    elif choice == "2":
                        self._register()
                    else:
                        self._output("Opción no válida.")
                except (ValueError, LookupError, PermissionError) as error:
                    self._output(str(error))
                except (ConnectionError, mysql.connector.Error):
                    self._output("No se pudo completar la operación de persistencia.")
                except RuntimeError:
                    self._output("Se detectó un estado de datos no válido.")
                continue

            self._show_authenticated_menu(user.role)
            choice = self._input("Opción: ").strip()
            if choice == "0":
                self._auth.logout()
                self._output("Sesión cerrada.")
                continue
            try:
                self._dispatch(choice, user.user_id)
            except (ValueError, LookupError, PermissionError) as error:
                self._output(str(error))
            except (ConnectionError, mysql.connector.Error):
                self._output("No se pudo completar la operación de persistencia.")
            except RuntimeError:
                self._output("Se detectó un estado de datos no válido.")

    def _login(self) -> None:
        email = self._input("Correo: ")
        password = self._password("Contraseña: ")
        user = self._auth.login(email, password)
        self._output(f"Bienvenida/o, {user.full_name}.")

    def _register(self) -> None:
        name = self._input("Nombre: ")
        email = self._input("Correo: ")
        password = self._password("Contraseña (mínimo 10 caracteres): ")
        confirmation = self._password("Confirme la contraseña: ")
        if password != confirmation:
            raise ValueError("Las contraseñas no coinciden.")
        user = self._auth.register(name, email, password)
        self._output(f"Cuenta creada (ID {user.user_id}). Inicie sesión.")

    def _show_authenticated_menu(self, role: str) -> None:
        self._output("\n1) Consultar destinos  2) Consultar paquetes")
        self._output("3) Reservar paquete  4) Mis reservas")
        self._output("5) Cancelar una de mis reservas")
        if role == "admin":
            self._output(
                "6) Crear destino  7) Modificar destino  8) Eliminar destino"
            )
            self._output(
                "9) Crear paquete  10) Modificar paquete  11) Eliminar paquete"
            )
            self._output(
                "12) Todas las reservas  13) Cambiar estado  14) Consultar usuarios"
            )
        self._output("0) Cerrar sesión")

    def _dispatch(self, choice: str, user_id: int | None) -> None:
        actions: dict[str, Callable[[], None]] = {
            "1": self._list_destinations,
            "2": self._list_packages,
            "3": lambda: self._create_reservation(user_id),
            "4": lambda: self._list_reservations(user_id),
            "5": lambda: self._cancel_own_reservation(user_id),
        }
        admin_actions: dict[str, Callable[[], None]] = {
            "6": self._create_destination,
            "7": self._update_destination,
            "8": self._delete_destination,
            "9": self._create_package,
            "10": self._update_package,
            "11": self._delete_package,
            "12": lambda: self._list_reservations(None),
            "13": self._change_reservation_status,
            "14": self._list_users,
        }
        if choice in admin_actions:
            self._auth.require_role("admin")
            admin_actions[choice]()
        elif choice in actions:
            actions[choice]()
        else:
            self._output("Opción no válida.")

    def _read_id(self, prompt: str) -> int:
        try:
            identifier = int(self._input(prompt))
        except ValueError:
            raise ValueError("Ingrese un identificador numérico.") from None
        if identifier <= 0:
            raise ValueError("El identificador debe ser positivo.")
        return identifier

    def _read_date(self, prompt: str) -> date:
        try:
            return date.fromisoformat(self._input(prompt).strip())
        except ValueError:
            raise ValueError("Use una fecha válida con formato AAAA-MM-DD.") from None

    def _read_destination_ids(self) -> list[int]:
        try:
            ids = [int(value.strip()) for value in self._input(
                "IDs de destinos separados por coma: "
            ).split(",")]
        except ValueError:
            raise ValueError("Los IDs deben ser números separados por coma.") from None
        if not ids or any(item <= 0 for item in ids):
            raise ValueError("Debe indicar identificadores positivos.")
        return ids

    def _prompt_package(self) -> TravelPackage:
        name = self._input("Nombre: ")
        description = self._input("Descripción: ")
        start = self._read_date("Fecha de inicio (AAAA-MM-DD): ")
        end = self._read_date("Fecha de término (AAAA-MM-DD): ")
        try:
            price = Decimal(self._input("Precio por viajero: ").strip())
            slots = int(self._input("Disponibilidad de viajeros: "))
        except (ValueError, ArithmeticError):
            raise ValueError("Precio y disponibilidad deben ser números válidos.") from None
        return TravelPackage(
            name,
            description,
            start,
            end,
            price,
            slots,
            self._read_destination_ids(),
        )

    def _list_destinations(self) -> None:
        destinations = self._destinations.list_all()
        if not destinations:
            self._output("No hay destinos registrados.")
        for item in destinations:
            self._output(
                f"{item.destination_id}: {item.name}, {item.country} — {item.description}"
            )

    def _create_destination(self) -> None:
        destination = Destination(
            self._input("Nombre: "),
            self._input("País: "),
            self._input("Descripción: "),
        )
        self._output(f"Destino creado (ID {self._destinations.create(destination)}).")

    def _update_destination(self) -> None:
        destination_id = self._read_id("ID del destino: ")
        destination = Destination(
            self._input("Nuevo nombre: "),
            self._input("Nuevo país: "),
            self._input("Nueva descripción: "),
        )
        self._destinations.update(destination_id, destination)
        self._output("Destino actualizado.")

    def _delete_destination(self) -> None:
        self._destinations.delete(self._read_id("ID del destino: "))
        self._output("Destino eliminado.")

    def _list_packages(self) -> None:
        packages = self._packages.list_all()
        if not packages:
            self._output("No hay paquetes registrados.")
        for item in packages:
            self._output(
                f"{item.package_id}: {item.name}; {item.start_date} a {item.end_date}; "
                f"{item.duration_days} días; ${item.unit_price} por viajero; "
                f"disponibles: {item.available_slots}; destinos: {item.destination_ids}"
            )

    def _create_package(self) -> None:
        package = self._prompt_package()
        package_id = self._packages.create(package)
        self._output(f"Paquete creado (ID {package_id}).")

    def _update_package(self) -> None:
        package_id = self._read_id("ID del paquete: ")
        package = self._prompt_package()
        self._packages.update(package_id, package)
        self._output("Paquete actualizado.")

    def _delete_package(self) -> None:
        self._packages.delete(self._read_id("ID del paquete: "))
        self._output("Paquete eliminado.")

    def _create_reservation(self, user_id: int | None) -> None:
        if user_id is None:
            raise PermissionError("Inicie sesión para reservar.")
        package_id = self._read_id("ID del paquete: ")
        travelers = self._read_id("Cantidad de viajeros: ")
        reservation = self._reservations.create(user_id, package_id, travelers)
        self._output(
            f"Reserva {reservation.reservation_id} confirmada. "
            f"Total: ${reservation.total_price}."
        )

    def _list_reservations(self, user_id: int | None) -> None:
        if user_id is None:
            self._auth.require_role("admin")
            reservations = self._reservations.list_all()
        else:
            reservations = self._reservations.list_by_user(user_id)
        if not reservations:
            self._output("No hay reservas registradas.")
        for item in reservations:
            self._output(self._reservation_text(item))

    @staticmethod
    def _reservation_text(reservation: Reservation) -> str:
        return (
            f"{reservation.reservation_id}: paquete {reservation.package_id}; "
            f"viajeros {reservation.travelers}; total ${reservation.total_price}; "
            f"estado {reservation.status}"
        )

    def _cancel_own_reservation(self, user_id: int | None) -> None:
        if user_id is None:
            raise PermissionError("Inicie sesión para gestionar reservas.")
        reservation_id = self._read_id("ID de la reserva: ")
        reservation = self._reservations.get_by_id(reservation_id)
        if reservation.user_id != user_id:
            raise PermissionError("No puede modificar una reserva de otra persona.")
        self._reservations.cancel(reservation_id)
        self._output("Reserva cancelada.")

    def _change_reservation_status(self) -> None:
        reservation_id = self._read_id("ID de la reserva: ")
        status = self._input("Estado (confirmed/cancelled): ").strip().lower()
        self._reservations.update_status(reservation_id, status)
        self._output("Estado de reserva actualizado.")

    def _list_users(self) -> None:
        self._auth.require_role("admin")
        for user in self._users.list_all():
            self._output(f"{user.user_id}: {user.full_name} — {user.email} ({user.role})")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Gestión de Viajes Aventura")
    operations = parser.add_mutually_exclusive_group()
    operations.add_argument(
        "--bootstrap-admin",
        action="store_true",
        help="crear la única cuenta administradora inicial",
    )
    operations.add_argument(
        "--initialize-schema",
        action="store_true",
        help="crear tablas idempotentemente (requiere permiso CREATE)",
    )
    arguments = parser.parse_args()
    application = ViajesConsole()
    try:
        if arguments.bootstrap_admin:
            verify_tables()
            application.bootstrap_admin()
            return 0
        if arguments.initialize_schema:
            initialize_tables()
            print("Esquema de Viajes Aventura preparado.")
            return 0
        return application.run()
    except (ValueError, LookupError, PermissionError) as error:
        print(error)
        return 1
    except (ConnectionError, RuntimeError, mysql.connector.Error):
        print(
            "No se pudo iniciar Viajes Aventura. Verifique la conexión "
            "y los permisos de la base de datos."
        )
        return 1
