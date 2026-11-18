# Taller Clase 8 — Preparar el proyecto

## Alcance y estado

El material compartido identifica tres componentes para el prototipo: `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo. El UML original de la evaluación anterior no está en el repositorio. Por eso, los atributos y reglas mínimos documentados aquí son una **propuesta de referencia pendiente de validación**, no una afirmación de que el UML sea oficial o esté aprobado.

Las casillas marcan el estado de preparación local. Una casilla marcada no implica aprobación del equipo/docente ni que una tarea haya sido registrada en Jira.

## Checklist de las diez actividades

- [ ] **1. Revisar y corregir el UML.** Se documentó un modelo de referencia; falta compararlo y corregirlo según el UML original y obtener la validación correspondiente.
- [x] **2. Definir tres componentes nuevos.** Se prepararon `Department`, `Project` y `WorkRecord`; `Employee` se considera entidad de apoyo según el material compartido.
- [x] **3. Asignar responsable principal a cada componente.** Pamela: `Department` y `Project`; Valentina: `WorkRecord`. La distribución final requiere acuerdo del equipo.
- [x] **4. Definir relaciones con otras clases.** Se registraron las multiplicidades de referencia; pendientes de comparación con el UML original.
- [x] **5. Diseñar las tablas necesarias.** Se preparó el esquema relacional inicial en `docs/database_model.md`; sus atributos aún son supuestos.
- [ ] **6. Crear ramas de trabajo.** No se crearon. Por indicación de la usuaria, se continúa en `setup/project-structure` y se pospone la creación de ramas.
- [x] **7. Crear la estructura de archivos.** Se agregaron ubicaciones mínimas para dominio, persistencia y pruebas.
- [x] **8. Crear clases y DAO iniciales.** Se implementó el prototipo inicial, separado por responsabilidad.
- [x] **9. Conseguir al menos un INSERT funcional por componente.** La ejecución local insertó Department, Project y WorkRecord, además de Employee como apoyo; las pruebas también verifican las relaciones.
- [x] **10. Registrar problemas pendientes.** Se documentaron en este archivo y en los documentos relacionados.

## Componentes y asignación propuesta

Los nombres son los indicados por el material de trabajo. Las responsabilidades del negocio deben confirmarse contra el UML original.

| Componente | Responsable principal propuesto | Clase/DAO de referencia | Relación de referencia |
|---|---|---|---|
| `Department` | Pamela | `Department` / `DepartmentDAO` | Un departamento tiene `0..*` empleados. |
| `Project` | Pamela | `Project` / `ProjectDAO` | Un proyecto tiene `0..*` registros de trabajo. |
| `WorkRecord` | Valentina | `WorkRecord` / `WorkRecordDAO` | Cada registro enlaza un empleado y un proyecto. |
| `Employee` (apoyo) | Compartido para integración | `Employee` / `EmployeeDAO` | Cada empleado se asocia a un departamento; un empleado tiene `0..*` registros. |

Pamela y Valentina colaboran en UML, integración, pruebas generales y revisión. La asignación definitiva requiere acuerdo entre ambas. No se afirma que Valentina tenga permisos de repositorio configurados.

## Relaciones de referencia

- `Department 1 — 0..* Employee`.
- `Employee 1 — 0..* WorkRecord`.
- `Project 1 — 0..* WorkRecord`.

El detalle de atributos, tipos y restricciones está en `docs/uml.md` y `docs/database_model.md`, marcado como propuesta.

## Estructura inicial preparada

- `src/domain/`: entidades con validaciones sencillas.
- `src/persistence/`: conexión SQLite, creación de tablas y DAO de inserción.
- `src/main.py`: demostración del flujo de inserción.
- `tests/`: pruebas del dominio, esquema, DAO e integridad referencial.

No se agregan `Service`, `Controller`, DAO genérico ni capas adicionales.

## Flujo de ramas propuesto

1. Mantener `main` estable y evitar cambios directos.
2. Desde `main` actualizado, Pamela trabajaría en `feature/pamela-department-project`.
3. Valentina trabajaría en `feature/valentina-work-record`.
4. Integrar mediante `integration/class8` si el equipo mantiene esa estrategia; abrir Pull Requests y solicitar revisión mutua antes de integrar a `main`.
5. Ejecutar las pruebas acordadas antes de completar la integración.

Las ramas anteriores son nombres propuestos, no están creadas. En esta sesión se continúa en `setup/project-structure` por autorización de la usuaria; no se hizo commit, push, merge ni Pull Request.

## Bloqueos y decisiones pendientes

1. Conseguir el UML original de la evaluación anterior y confirmar el modelo con el equipo/docente.
2. Confirmar atributos, métodos y reglas de negocio reales; en particular `name`, `work_date` y `hours`.
3. Acordar la distribución definitiva y el liderazgo de la entidad de apoyo `Employee`.
4. Confirmar acceso y permisos de Valentina al repositorio, sin presumirlos.
5. Confirmar la integración de ramas cuando el equipo autorice crearlas.
6. Revisar resultados de pruebas e inserciones antes de declarar el taller terminado.
7. Registrar cualquier ajuste al esquema y al motor SQLite en `docs/decisions.md`.
