# Decisiones técnicas — Viajes Aventura

## Decisiones implementadas

| ID | Decisión | Justificación |
|---|---|---|
| D-01 | MariaDB/MySQL Connector existente; `127.0.0.1:3307`, base `viajes_aventura`. | Mantiene los parámetros entregados y la conexión ya probada unitariamente. |
| D-02 | Tablas InnoDB con `utf8mb4`, PK/FK/checks e índices; DDL `IF NOT EXISTS`. | Integridad y creación repetible sin borrar datos. |
| D-03 | Tabla puente `package_destinations`. | Modela correctamente la relación N:M entre paquetes y destinos. |
| D-04 | Unidades monetarias `Decimal`; precio total centralizado en `TravelPackage.calculate_total`. | Evita errores de coma flotante y duplicación de la regla. |
| D-05 | DAO separados por entidad, SQL parametrizado y transacciones. | Separa dominio/persistencia y mantiene consistencia en relaciones/reservas. |
| D-06 | Hash `hashlib.pbkdf2_hmac("sha256")`, 600 000 iteraciones y sal aleatoria de 16 bytes. | Alternativa disponible en biblioteca estándar; evita agregar dependencias. Se usa `hmac.compare_digest` al verificar. |
| D-07 | Registro público crea rol `customer`; bootstrap crea un solo admin con bloqueo MariaDB. | Impide que el usuario elija su propio rol al registrarse. |
| D-08 | `src/viajes_main.py` separado del `src/main.py` histórico. | No altera el menú ni las funciones EcoTech. |
| D-09 | Pruebas unitarias con mocks; integración MariaDB separada y optativa. | Pasaron 45 pruebas, incluidas cuatro integraciones. La prueba concurrente usó dos conexiones independientes y limpió exclusivamente los IDs creados. |
| D-10 | Inicialización DDL explícita; el menú solo verifica esquema y usa permisos DML. | Aplica mínimo privilegio después del aprovisionamiento inicial. |

## Protección de información

- Las credenciales de DB continúan en `VIAJES_DB_USER` y `VIAJES_DB_PASSWORD`; no se copiaron ni imprimieron.
- El archivo `.env` no se leyó ni modificó. No incluirlo en entregas ni Git.
- Contraseñas de usuarios nunca se guardan en texto plano; PBKDF2 no es cifrado reversible.
- Las consultas usan parámetros; la interfaz oculta mensajes internos de MySQL.
- Las pruebas de integración deben usar filas creadas exclusivamente para la prueba y limpieza/rollback controlados, nunca borrar datos ajenos.

## Uso y evaluación crítica de código generado con IA

Se usó asistencia de IA para proponer/editar módulos y documentación de esta implementación. La salida se trató como código no confiable: se contrastó con la arquitectura local, la configuración establecida y las pruebas ejecutadas. Las pruebas unitarias cubren validación, hash, SQL parametrizado simulado, relaciones, transacciones y restricciones de disponibilidad; las pruebas integradas comprobaron contra MariaDB la conexión, inicialización de esquema, CRUD, autenticación, roles y ciclo de reservas, incluida la concurrencia del último cupo.

Limitaciones conocidas que requieren revisión humana: no se registró la versión exacta de MariaDB; `CREATE TABLE IF NOT EXISTS` no migra una tabla existente con columnas diferentes; no se completó una demostración autenticada en terminal real, porque `getpass` impidió automatizarla con entrada redirigida (los roles sí se ejercitaron con entradas controladas); el modelo/rúbrica y los diagramas requieren revisión académica. No se afirma aprobación del equipo/docente ni se inventan evidencias.

## Pendientes de confirmar

- La inicialización real y las pruebas integradas se ejecutaron después de habilitar `CREATE`; las cinco tablas y sus metadatos fueron verificados.
- La integración usa registros únicos y elimina únicamente los IDs que creó; la comprobación posterior no encontró filas temporales residuales.
- Revisar si la rúbrica requiere evidencia adicional o una demostración guiada del menú.
- Confirmar alcance y modelo con el equipo y la rúbrica; no hay fechas/Jira verificados.
- No crear dependencias adicionales sin justificar necesidad.
