# UML de clases — Viajes Aventura

## Alcance

Este diagrama describe el modelo que implementa el código del proyecto Viajes Aventura. Es una propuesta técnica de esta entrega; aprobación por el equipo/docente queda pendiente de confirmar.

```mermaid
classDiagram
    class User {
        -int? user_id
        -str full_name
        -str email
        -str role
        +assign_id(int) None
    }
    class Destination {
        -int? destination_id
        -str name
        -str country
        -str description
        +update(str, str, str) None
        +assign_id(int) None
    }
    class TravelPackage {
        -int? package_id
        -str name
        -str description
        -date start_date
        -date end_date
        -Decimal unit_price
        -int available_slots
        -tuple destination_ids
        +duration_days int
        +calculate_total(int) Decimal
        +assign_id(int) None
    }
    class Reservation {
        -int? reservation_id
        -int user_id
        -int package_id
        -int travelers
        -Decimal unit_price
        -Decimal total_price
        -str status
        -datetime booked_at
        +cancel() None
        +assign_id(int) None
    }
    class DestinationDAO {
        +create(Destination) int
        +list_all() list
        +get_by_id(int) Destination
        +update(int, Destination) None
        +delete(int) None
    }
    class TravelPackageDAO {
        +create(TravelPackage) int
        +list_all() list
        +get_by_id(int) TravelPackage
        +get_destinations(int) list
        +update(int, TravelPackage) None
        +delete(int) None
    }
    class UserDAO {
        +create(User, str) int
        +get_by_id(int) User
        +find_by_email(str) User?
        +list_all() list
    }
    class ReservationDAO {
        +create(int, int, int) Reservation
        +get_by_id(int) Reservation
        +list_by_user(int) list
        +list_all() list
        +update_status(int, str) None
        +cancel(int) None
    }
    class AuthenticationService {
        +register(str, str, str) User
        +login(str, str) User
        +logout() None
        +require_role(str) User
    }
    class PasswordHash {
        +hash_password(str) str
        +verify_password(str, str) bool
    }

    User "1" --> "0..*" Reservation : realiza
    TravelPackage "1" --> "0..*" Reservation : recibe
    TravelPackage "1..*" --> "0..*" Destination : package_destinations
    DestinationDAO ..> Destination : persiste
    TravelPackageDAO ..> TravelPackage : persiste
    UserDAO ..> User : persiste
    ReservationDAO ..> Reservation : persiste
    AuthenticationService ..> UserDAO : autentica
    AuthenticationService ..> PasswordHash : verifica
```

## Responsabilidades y reglas relevantes

- Las entidades validan sus valores y mantienen campos privados con propiedades de lectura.
- `TravelPackage.calculate_total()` es la operación central de precio total: precio unitario multiplicado por viajeros, con `Decimal`.
- La duración se calcula inclusivamente a partir de las fechas.
- El paquete requiere al menos un destino; el DAO persiste el vínculo N:M de forma transaccional.
- `User` no guarda ni expone la contraseña en claro; el hash se maneja por el servicio/DAO de autenticación.
- `Reservation` conserva el precio unitario de la compra y controla la transición local de cancelación.
- Los DAO dependen de la conexión MySQL existente y no pertenecen al dominio.

## Límites / confirmación pendiente

El modelo relacional se detalla en `database_model.md`. La asociación UML de paquetes y destinos se realiza mediante IDs y la tabla intermedia, no mediante listas de objetos en memoria. El equipo debe confirmar nombres/campos y que las reglas académicas coinciden con la rúbrica; no se afirma aprobación docente.
