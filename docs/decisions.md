# Decisiones técnicas

## 1. Decisiones confirmadas
| ID | Decisión | Razón |
|----|----------|-------|
| D-01 | Lenguaje: Python. | Requisito de la asignatura. |
| D-02 | Código, archivos, tablas y columnas en inglés. | Convención del proyecto. |
| D-03 | Documentación y mensajes al usuario en español. | Convención del proyecto. |
| D-04 | Gestión ágil con Jira (Kanban) y control de versiones con GitHub. | Requisito de la asignatura. |
| D-05 | No trabajar sobre `main`; usar ramas y Pull Requests. | Proteger la rama principal y permitir revisión. |
| D-06 | Estructura inicial mínima, ampliable por etapas. | Evitar implementaciones adelantadas. |
| D-07 | No subir credenciales ni bases de datos (`.gitignore`). | Seguridad. |

## 2. Decisiones pendientes
| ID | Tema | Opciones | Razón de la pendiente |
|----|------|----------|-----------------------|
| P-01 | Caso de negocio y entidades | **[PENDIENTE]** | Depende del enunciado y UML validado. |
| P-02 | Base de datos | SQLite o MySQL | SQLite no requiere servidor; MySQL requiere credenciales y `.env`. |
| P-03 | Interfaz con el usuario | Consola u otra | No definida. |
| P-04 | Herramienta de pruebas | `unittest` o `pytest` | `unittest` no requiere instalar nada. |
| P-05 | Responsables de cada tarjeta | Acordar P y V | Se decide en la planificación. |
| P-06 | Versión mínima de Python | **[PENDIENTE]** (README sugiere 3.10+) | Confirmar con el equipo. |

## 3. Supuestos del prototipo Clase 8

El material compartido propone `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo, y SQLite para el ejercicio inicial. La propuesta de UML, esquema y asignación aún debe compararse con el modelo original y acordarse con el equipo.

| Supuesto | Revisión pendiente |
|---|---|
| Se usan claves enteras, `name`, y para `WorkRecord`, `work_date` y `hours`. | Confirmar nombres, tipos y atributos completos con el UML original. |
| `Employee` requiere `department_id`; `WorkRecord` requiere `employee_id` y `project_id`. | Confirmar obligatoriedad y multiplicidades. |
| `hours` debe ser positivo y `work_date` se almacena como texto ISO 8601. | Confirmar reglas y formato de datos. |
| Se usa SQLite mediante `sqlite3` para el prototipo. | Reconfirmar con el equipo si el alcance cambia. |

No se declara que el UML de referencia haya sido validado por el equipo o por el docente.

## 4. Decisiones de colaboración pendientes

- Confirmar la distribución definitiva de responsabilidades.
- Crear las ramas propuestas solo cuando el equipo autorice y confirme acceso.
- Confirmar acceso de Valentina al repositorio; no se presume que ya tenga permisos.
