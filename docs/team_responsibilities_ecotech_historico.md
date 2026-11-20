# Distribuci├│n de responsabilidades ÔÇö propuesta Clase 8

La distribuci├│n refleja la asignaci├│n indicada en el material del taller. Debe ser acordada por Pamela y Valentina. No se afirma que ambas tengan ya acceso o permisos configurados en GitHub.

| Integrante | Componente | Clase | DAO | Tabla | Rama propuesta (no creada) | Responsabilidades | Evidencia esperada |
|---|---|---|---|---|---|---|---|
| Pamela | `Department` | `Department` | `DepartmentDAO` | `departments` | `feature/pamela-department-project` | Liderar el componente, apoyar su relaci├│n con `Employee` e integrar estructura y revisi├│n del repositorio. | Prueba de validaci├│n e inserci├│n; revisi├│n del equipo. |
| Pamela | `Project` | `Project` | `ProjectDAO` | `projects` | `feature/pamela-department-project` | Liderar el componente y revisar su relaci├│n con `WorkRecord`. | Prueba de inserci├│n y revisi├│n del equipo. |
| Valentina | `WorkRecord` | `WorkRecord` | `WorkRecordDAO` | `work_records` | `feature/valentina-work-record` | Liderar el componente, revisar sus relaciones con `Employee` y `Project`, y verificar sus inserciones. | Prueba de inserci├│n con ambas claves for├íneas. |
| Compartido | Entidad de apoyo | `Employee` | `EmployeeDAO` | `employees` | `integration/class8` | Coordinar la entidad necesaria para las relaciones y la integraci├│n del flujo. | Prueba de inserci├│n asociada a un departamento. |
| Ambas | Integraci├│n y revisi├│n | ÔÇö | ÔÇö | ÔÇö | `integration/class8` | Revisar el UML de referencia, integrar cambios, ejecutar pruebas y realizar revisi├│n por Pull Request cuando las ramas est├®n disponibles. | Revisi├│n acordada y pruebas ejecutadas. |
| Valentina | Seguimiento | ÔÇö | ÔÇö | ÔÇö | Seg├║n acuerdo del equipo | Preparar y organizar las tarjetas para el tablero Jira/Kanban. | Tareas listas para registrar; no se afirma que ya se hayan creado en Jira. |

Las ramas son nombres propuestos en el material compartido. En esta sesi├│n no se crearon por decisi├│n de continuar en la rama actual.
