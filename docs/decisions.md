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
