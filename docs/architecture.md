# Arquitectura — Viajes Aventura

## Capas actuales

- `src/viajes/domain/`: `User`, `Destination`, `TravelPackage`, `Reservation` y validaciones. No ejecuta SQL.
- `src/viajes/persistence/`: esquema idempotente y DAO especializados para destinos, paquetes, usuarios y reservas; consultas parametrizadas.
- `src/viajes/auth.py`: hash/verificación de contraseñas, registro, inicio/cierre de sesión y control de rol.
- `src/viajes/cli.py`: interfaz de consola con acciones de cliente y administrador.
- `src/viajes_main.py`: punto de entrada separado para Viajes Aventura.
- `src/persistence/viajes_connection.py`: conexión configurada para MariaDB/MySQL y credenciales del entorno.
- `src/main.py`, `src/domain/` y DAO sin prefijo turístico: prototipo EcoTech/SQLite preexistente, no utilizado por Viajes.

## Flujos de persistencia

- Un DAO abre/cierra su conexión y cursor; las consultas usan parámetros `%s`.
- Crear/actualizar paquete y tabla intermedia se realizan en una transacción.
- Reservar bloquea la fila del paquete con `FOR UPDATE`, valida cupos/fechas y confirma el descuento junto con la reserva; cualquier excepción produce `rollback`.
- Los cambios de estado de reserva ajustan los cupos en la misma transacción.
- El DDL usa InnoDB y `CREATE TABLE IF NOT EXISTS`; en MariaDB el DDL puede confirmar implícitamente y no se presenta como migración transaccional.
- La inicialización explícita del esquema requiere `CREATE`; el menú normal solo verifica las cinco tablas mediante `information_schema` y no necesita privilegios DDL permanentes.

## Decisiones de diseño

No se introducen ORM, DAO genérico ni dependencias de hashing. Las entidades turísticas están bajo un paquete propio para evitar colisiones con el modelo EcoTech. Las credenciales se obtienen mediante `VIAJES_DB_USER` y `VIAJES_DB_PASSWORD`; no se muestran ni se incorporan a esta documentación.

La autenticación es una sesión en memoria del proceso de consola, no un sistema web con cookies/tokens. Roles soportados: `customer` y `admin`; registro público solo crea clientes. La creación del primer administrador está protegida por un bloqueo de base de datos y se invoca mediante opción explícita de bootstrap.

## Estado de validación

La ejecución completa aprobó 45 pruebas, incluidas cuatro pruebas de integración MariaDB. Se verificaron conexión, inicialización del esquema, CRUD, autenticación, roles, reservas, disponibilidad, cancelación/reapertura y concurrencia del último cupo con dos conexiones independientes. Cada fila de prueba se eliminó por su identificador exacto; la comprobación posterior no encontró registros temporales residuales.

La aplicación se inició para revisar el menú inicial y los flujos de cliente/administrador se probaron con entradas controladas. No se completó una demostración autenticada en terminal real: `getpass` impidió automatizar el inicio de sesión mediante entrada redirigida.
