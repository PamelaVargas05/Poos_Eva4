# Distribución de responsabilidades — propuesta Clase 8

La distribución refleja la asignación indicada en el material del taller. Debe ser acordada por Pamela y Valentina. No se afirma que ambas tengan ya acceso o permisos configurados en GitHub.

| Integrante | Componente | Clase | DAO | Tabla | Rama propuesta (no creada) | Responsabilidades | Evidencia esperada |
|---|---|---|---|---|---|---|---|
| Pamela | `Department` | `Department` | `DepartmentDAO` | `departments` | `feature/pamela-department-project` | Liderar el componente, apoyar su relación con `Employee` e integrar estructura y revisión del repositorio. | Prueba de validación e inserción; revisión del equipo. |
| Pamela | `Project` | `Project` | `ProjectDAO` | `projects` | `feature/pamela-department-project` | Liderar el componente y revisar su relación con `WorkRecord`. | Prueba de inserción y revisión del equipo. |
| Valentina | `WorkRecord` | `WorkRecord` | `WorkRecordDAO` | `work_records` | `feature/valentina-work-record` | Liderar el componente, revisar sus relaciones con `Employee` y `Project`, y verificar sus inserciones. | Prueba de inserción con ambas claves foráneas. |
| Compartido | Entidad de apoyo | `Employee` | `EmployeeDAO` | `employees` | `integration/class8` | Coordinar la entidad necesaria para las relaciones y la integración del flujo. | Prueba de inserción asociada a un departamento. |
| Ambas | Integración y revisión | — | — | — | `integration/class8` | Revisar el UML de referencia, integrar cambios, ejecutar pruebas y realizar revisión por Pull Request cuando las ramas estén disponibles. | Revisión acordada y pruebas ejecutadas. |
| Valentina | Seguimiento | — | — | — | Según acuerdo del equipo | Preparar y organizar las tarjetas para el tablero Jira/Kanban. | Tareas listas para registrar; no se afirma que ya se hayan creado en Jira. |

Las ramas son nombres propuestos en el material compartido. En esta sesión no se crearon por decisión de continuar en la rama actual.
