# Pruebas automatizadas

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Ese comando omite las integraciones MariaDB por defecto. Para ejecutar la suite completa con MariaDB configurada:

```powershell
$env:VIAJES_RUN_INTEGRATION_TESTS = '1'
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

- `test_domain.py` y `test_persistence.py` verifican el prototipo histórico EcoTech con SQLite en memoria.
- `test_viajes_persistence.py` conserva las seis pruebas existentes de conexión e inicialización.
- `test_viajes_schema.py`, `test_viajes_domain.py`, `test_viajes_daos.py` y `test_viajes_auth.py` prueban la aplicación turística con mocks/unit tests; no usan WampServer ni modifican bases de datos.
- `tests/integration/test_viajes_mariadb.py` contiene cuatro pruebas separadas y omitidas por defecto. Con `VIAJES_RUN_INTEGRATION_TESTS=1` verifica conexión/esquema, CRUD, autenticación, roles, disponibilidad, cancelaciones y concurrencia del último cupo con datos de prueba aislados. Cada fila creada se limpia por su PK exacta.

La ejecución completa con `VIAJES_RUN_INTEGRATION_TESTS=1` aprobó 45 pruebas, incluidas las cuatro integraciones MariaDB. Se comprobó que la prueba concurrente deja una sola reserva confirmada para el último cupo, disponibilidad no negativa y relaciones consistentes. Las pruebas no borran filas preexistentes.
