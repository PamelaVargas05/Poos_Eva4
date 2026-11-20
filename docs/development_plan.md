# Plan de desarrollo — Viajes Aventura

## Product Backlog propuesto

El backlog refleja el alcance académico solicitado. No se afirma que estas historias estén cargadas en Jira ni que hayan sido asignadas a una integrante.

| ID | Elemento | Prioridad | Estado en el código local |
|---|---|---|---|
| PB-01 | Configuración segura de conexión y esquema idempotente. | Alta | Esquema MariaDB inicializado y verificado. |
| PB-02 | Entidades y reglas de destinos, paquetes, usuarios y reservas. | Alta | Implementadas y con pruebas unitarias. |
| PB-03 | CRUD de destinos y paquetes, relación N:M con destinos. | Alta | CRUD real verificado con datos aislados. |
| PB-04 | Registro, autenticación, roles y bootstrap del primer administrador. | Alta | Pruebas unitarias e integración MariaDB pasaron. |
| PB-05 | Reservas, disponibilidad, historial y cambios de estado. | Alta | Ciclo real de reserva/cancelación/reapertura y concurrencia del último cupo verificados. |
| PB-06 | Menú independiente de Viajes Aventura. | Alta | Menú inicial y roles ejercitados con entradas controladas; demostración autenticada en terminal real pendiente por la limitación de `getpass` con entrada redirigida. |
| PB-07 | Suite de pruebas unitaria e integración controlada. | Alta | 45 pruebas aprobadas, incluidas cuatro integraciones MariaDB. |
| PB-08 | UML, modelo, requisitos, seguridad y evaluación de IA. | Media | Documentación actualizada; revisión del equipo pendiente. |
| PB-09 | Validación de entregables contra rúbrica y acuerdo del equipo. | Alta | Pendiente de confirmar. |

## Sprint Backlog sugerido

| Orden | Tarea | Criterio de aceptación | Estado local |
|---|---|---|---|
| 1 | Revisar modelo, reglas y esquema con el equipo/docente. | Atributos, cardinalidades y decisiones quedan acordados y documentados. | Pendiente de confirmación |
| 2 | Ejecutar inicialización idempotente en el MariaDB autorizado. | Tablas de Viajes presentes y datos existentes preservados. | Ejecutado y verificado |
| 3 | Ejecutar CRUD, reservas y concurrencia controlada contra MariaDB. | Integridad, disponibilidad y rollback verificados con datos exclusivos de prueba. | Ejecutado; suite integrada aprobada |
| 4 | Hacer revisión cruzada de código y pruebas. | Observaciones registradas; sin atribuir aprobación antes de que ocurra. | Pendiente de realizar por el equipo |
| 5 | Verificar documentación/evidencias con la rúbrica real. | Entregables y evidencia existentes; pendientes etiquetados. | Pendiente de confirmar |

Estas tareas son una propuesta de trabajo, no registros de Jira ni evidencia de que integrantes hayan realizado reuniones o revisiones.

## Fases y entregables

| Fase | Entregable | Estado / condición |
|---|---|---|
| Análisis y modelo | Requerimientos, casos de uso, BPMN conceptual, UML y modelo relacional. | Documentados; validación del equipo/docente pendiente. |
| Implementación | Entidades, esquema, DAO, autenticación y CLI. | Código local implementado. |
| Pruebas | Unitarias/simuladas e integración MariaDB aislada. | Suite completa ejecutada: 45 pruebas aprobadas, incluidas cuatro integraciones. |
| Cierre académico | Revisión de rúbrica, evidencia, backlog y responsabilidades. | Pendiente de confirmar por el equipo. |

## Cronograma

No se proporcionaron fechas oficiales de sprint ni entrega. Definir inicio, duración, revisiones y fecha final con el equipo; no se inventan hitos ni reuniones.
