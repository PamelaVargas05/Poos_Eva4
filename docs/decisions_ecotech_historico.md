# Decisiones t├®cnicas

## 1. Decisiones confirmadas
| ID | Decisi├│n | Raz├│n |
|----|----------|-------|
| D-01 | Lenguaje: Python. | Requisito de la asignatura. |
| D-02 | C├│digo, archivos, tablas y columnas en ingl├®s. | Convenci├│n del proyecto. |
| D-03 | Documentaci├│n y mensajes al usuario en espa├▒ol. | Convenci├│n del proyecto. |
| D-04 | Gesti├│n ├ígil con Jira (Kanban) y control de versiones con GitHub. | Requisito de la asignatura. |
| D-05 | No trabajar sobre `main`; usar ramas y Pull Requests. | Proteger la rama principal y permitir revisi├│n. |
| D-06 | Estructura inicial m├¡nima, ampliable por etapas. | Evitar implementaciones adelantadas. |
| D-07 | No subir credenciales ni bases de datos (`.gitignore`). | Seguridad. |

## 2. Decisiones pendientes
| ID | Tema | Opciones | Raz├│n de la pendiente |
|----|------|----------|-----------------------|
| P-01 | Caso de negocio y entidades | **[PENDIENTE]** | Depende del enunciado y UML validado. |
| P-02 | Base de datos | SQLite o MySQL | SQLite no requiere servidor; MySQL requiere credenciales y `.env`. |
| P-03 | Interfaz con el usuario | Consola u otra | No definida. |
| P-04 | Herramienta de pruebas | `unittest` o `pytest` | `unittest` no requiere instalar nada. |
| P-05 | Responsables de cada tarjeta | Acordar P y V | Se decide en la planificaci├│n. |
| P-06 | Versi├│n m├¡nima de Python | **[PENDIENTE]** (README sugiere 3.10+) | Confirmar con el equipo. |

## 3. Supuestos del prototipo Clase 8

El material compartido propone `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo, y SQLite para el ejercicio inicial. La propuesta de UML, esquema y asignaci├│n a├║n debe compararse con el modelo original y acordarse con el equipo.

| Supuesto | Revisi├│n pendiente |
|---|---|
| Se usan claves enteras, `name`, y para `WorkRecord`, `work_date` y `hours`. | Confirmar nombres, tipos y atributos completos con el UML original. |
| `Employee` requiere `department_id`; `WorkRecord` requiere `employee_id` y `project_id`. | Confirmar obligatoriedad y multiplicidades. |
| `hours` debe ser positivo y `work_date` se almacena como texto ISO 8601. | Confirmar reglas y formato de datos. |
| Se usa SQLite mediante `sqlite3` para el prototipo. | Reconfirmar con el equipo si el alcance cambia. |

No se declara que el UML de referencia haya sido validado por el equipo o por el docente.

## 4. Decisiones de colaboraci├│n pendientes

- Confirmar la distribuci├│n definitiva de responsabilidades.
- Crear las ramas propuestas solo cuando el equipo autorice y confirme acceso.
- Confirmar acceso de Valentina al repositorio; no se presume que ya tenga permisos.
