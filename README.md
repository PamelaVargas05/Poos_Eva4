# Viajes Aventura

Aplicación académica de gestión de destinos, paquetes turísticos, usuarios y reservas para TI3021 – Programación Orientada a Objetos Seguro (INACAP). Equipo informado por la usuaria: Pamela Vargas y Valentina Arias; la asignación de tareas y aprobaciones del equipo quedan pendientes de confirmar.

## Estado

La implementación incluye dominio turístico, esquema/DAO MariaDB, autenticación con hash, control de roles y menú de consola. En MariaDB se probaron la conexión, la inicialización de las cinco tablas, CRUD, autenticación, roles, reservas, disponibilidad, cancelaciones y una carrera controlada por el último cupo. La suite completa, ejecutada con la integración habilitada, aprobó 45 pruebas: 4 de integración MariaDB y las restantes unitarias/simuladas. Los datos temporales se limpiaron mediante sus identificadores exactos.

La implementación previa de EcoTech sigue separada: `src/main.py`, `src/domain/` y los DAO SQLite no se usan como entrada de Viajes Aventura y no fueron modificados.

Se ejecutó el punto de entrada para revisar el menú inicial. Los flujos de cliente y administrador se ejercitaron con entradas controladas; no se completó una demostración autenticada en terminal real, porque `getpass` no funciona correctamente al alimentar la aplicación mediante entrada redirigida.

## Componentes

```text
src/
├── main.py                         Punto de entrada histórico EcoTech
├── viajes_main.py                  Entrada Viajes Aventura
├── viajes/
│   ├── auth.py / passwords.py      Registro, roles y PBKDF2-HMAC
│   ├── cli.py                      Menú de consola
│   ├── domain/                     Usuario, destino, paquete, reserva
│   └── persistence/                Esquema y DAO MariaDB
└── persistence/
    ├── viajes_connection.py        Conexión existente de Viajes
    └── create_viajes_db.py         Inicializador existente (solo base)
```

Modelo relacional y relaciones: [docs/database_model.md](docs/database_model.md). Requerimientos, BPMN, casos de uso y trazabilidad: [docs/requirements.md](docs/requirements.md). UML de clases: [docs/uml.md](docs/uml.md). Decisiones y límites: [docs/decisions.md](docs/decisions.md).

## Configuración

Se conserva la configuración existente: host `127.0.0.1`, puerto `3307`, base `viajes_aventura`, charset `utf8mb4` y collation `utf8mb4_unicode_ci`. La conexión requiere `VIAJES_DB_USER` y `VIAJES_DB_PASSWORD` en el entorno o en `.env` local. El archivo `.env` no debe incluirse en Git ni compartirse; no se debe poner una contraseña en el código. No se muestra aquí ningún secreto.

Se requiere Python 3.10 o superior. `requirements.txt` declara las dependencias necesarias (`mysql-connector-python` y `python-dotenv`). La cuenta requiere permisos DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) para operar. El permiso `CREATE` se necesita al inicializar el esquema.

## Instalación, configuración e inicialización

Desde la raíz del proyecto, en PowerShell, crea el entorno virtual e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Configura las credenciales locales. Si aún no tienes un `.env`, puedes copiar la plantilla y reemplazar sus placeholders localmente. No sobrescribas un `.env` existente ni lo agregues a Git:

```powershell
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

La base `viajes_aventura` ya existe en el entorno configurado, por lo que normalmente no necesitas crearla. El siguiente comando es opcional, solo si la base no existe, y puede requerir privilegios `CREATE DATABASE`:

```powershell
.\.venv\Scripts\python.exe -B -m src.persistence.create_viajes_db
```

Inicializa idempotentemente las cinco tablas de Viajes Aventura. Este comando requiere permiso `CREATE` en la base y no borra tablas ni registros:

```powershell
.\.venv\Scripts\python.exe -B -m src.viajes.persistence.schema
```

Si todavía no existe un administrador, crea la única cuenta inicial. La contraseña se solicita sin mostrarla; ejecuta este comando en una terminal interactiva:

```powershell
.\.venv\Scripts\python.exe -B -m src.viajes_main --bootstrap-admin
```

Inicia la aplicación:

```powershell
.\.venv\Scripts\python.exe -B -m src.viajes_main
```

La aplicación normal solo verifica que el esquema exista, por lo que su cuenta operativa no necesita privilegios DDL permanentes. Si no tiene permiso para inicializar tablas, debe hacerlo una cuenta autorizada. El bootstrap solo funciona si aún no existe un administrador. Solo el administrador puede gestionar destinos/paquetes y consultar usuarios/todas las reservas; el registro normal crea clientes.

Para registrar e iniciar sesión como cliente, ejecutar el menú normal. Los paquetes requieren al menos un destino y reservas futuras solo se confirman si hay cupos disponibles.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Las pruebas unitarias/simuladas no usan WampServer, credenciales reales ni modifican bases de datos. Se mantienen las seis pruebas de `tests/test_viajes_persistence.py` y las pruebas previas de EcoTech. La integración MariaDB se habilita explícitamente y usa filas de prueba aisladas.

Las cuatro pruebas MariaDB son optativas por defecto. Para ejecutar la suite completa, incluidas las pruebas de integración (requiere MariaDB y credenciales locales), desde PowerShell:

```powershell
$env:VIAJES_RUN_INTEGRATION_TESTS = '1'
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Esta ejecución aprobó 45 pruebas, incluidas cuatro integraciones MariaDB. Se verificaron conexión, esquema, CRUD, autenticación, roles, ciclo de reservas y concurrencia del último cupo; las filas de prueba se limpiaron por sus IDs exactos.

## Documentación de evaluación

- Requerimientos priorizados, casos de uso, BPMN conceptual y trazabilidad: `docs/requirements.md`.
- Diagrama de clases y modelo de datos: `docs/uml.md`, `docs/database_model.md`.
- Product/Sprint Backlog, fases y fechas por confirmar: `docs/development_plan.md`.
- Roles/responsabilidades pendientes de acuerdo: `docs/team_responsibilities.md`.
- Tareas Jira como propuesta, no creadas: `docs/jira_tasks.md`.
- Seguridad y evaluación crítica de asistencia IA: `docs/decisions.md`.

Los documentos de Clase 8 que describen EcoTech se identifican como material histórico. No se inventan validaciones, reuniones, tareas Jira ni evidencias.
