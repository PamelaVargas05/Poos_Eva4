# Backlog propuesto para Jira — Viajes Aventura

> Borrador local para el equipo. No se afirma que se haya accedido a Jira, creado tarjetas, asignado personas o movido tareas de estado.

| ID sugerido | Tarea | Prioridad | Dependencia | Criterio de aceptación | Estado real |
|---|---|---|---|---|---|
| VA-01 | Confirmar alcance, modelo y reglas con la rúbrica. | Alta | Caso/rúbrica | Requerimientos, campos y cardinalidades acordados. | Pendiente de confirmar |
| VA-02 | Verificar conexión y esquema MariaDB en entorno autorizado. | Alta | VA-01 | Host/puerto/base revisados; tablas presentes sin borrar datos. | Verificado localmente |
| VA-03 | Validar CRUD de destinos y paquetes con MariaDB. | Alta | VA-02 | Create/read/update/delete y FK comprobados con datos de prueba aislados. | Integración local pasó |
| VA-04 | Validar registro, login, roles y protección de credenciales. | Alta | VA-02 | Hash no reversible, duplicados rechazados, mensajes genéricos. | Integración local pasó |
| VA-05 | Validar reservas, cancelación, disponibilidad y concurrencia. | Alta | VA-03, VA-04 | Cupos no negativos; rollback correcto; precio estable. | Ciclo y carrera de último cupo probados en MariaDB; una de dos conexiones confirmó la reserva |
| VA-06 | Revisar experiencia de menú y mensajes. | Media | VA-03 a VA-05 | Flujo cliente/admin ejercitado en el equipo. | Roles ejercitados con entradas controladas; demostración autenticada en terminal real pendiente por la limitación de `getpass` con entrada redirigida |
| VA-07 | Revisión cruzada de documentación y trazabilidad. | Media | VA-01 a VA-06 | README y docs alineados con el estado real y pauta. | Pendiente de confirmación |
| VA-08 | Recopilar evidencia final y confirmar responsabilidades. | Alta | VA-07 | Evidencias existentes, autoría correcta y pendientes explícitos. | Pendiente |

No se simulan comentarios, responsables, fechas, aprobaciones ni estados de Jira.
