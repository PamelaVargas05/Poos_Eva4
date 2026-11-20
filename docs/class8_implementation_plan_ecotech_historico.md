# Taller Clase 8 ÔÇö Preparar el proyecto

## Alcance y estado

El material compartido identifica tres componentes para el prototipo: `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo. El UML original de la evaluaci├│n anterior no est├í en el repositorio. Por eso, los atributos y reglas m├¡nimos documentados aqu├¡ son una **propuesta de referencia pendiente de validaci├│n**, no una afirmaci├│n de que el UML sea oficial o est├® aprobado.

Las casillas marcan el estado de preparaci├│n local. Una casilla marcada no implica aprobaci├│n del equipo/docente ni que una tarea haya sido registrada en Jira.

## Checklist de las diez actividades

- [ ] **1. Revisar y corregir el UML.** Se document├│ un modelo de referencia; falta compararlo y corregirlo seg├║n el UML original y obtener la validaci├│n correspondiente.
- [x] **2. Definir tres componentes nuevos.** Se prepararon `Department`, `Project` y `WorkRecord`; `Employee` se considera entidad de apoyo seg├║n el material compartido.
- [x] **3. Asignar responsable principal a cada componente.** Pamela: `Department` y `Project`; Valentina: `WorkRecord`. La distribuci├│n final requiere acuerdo del equipo.
- [x] **4. Definir relaciones con otras clases.** Se registraron las multiplicidades de referencia; pendientes de comparaci├│n con el UML original.
- [x] **5. Dise├▒ar las tablas necesarias.** Se prepar├│ el esquema relacional inicial en `docs/database_model.md`; sus atributos a├║n son supuestos.
- [ ] **6. Crear ramas de trabajo.** No se crearon. Por indicaci├│n de la usuaria, se contin├║a en `setup/project-structure` y se pospone la creaci├│n de ramas.
- [x] **7. Crear la estructura de archivos.** Se agregaron ubicaciones m├¡nimas para dominio, persistencia y pruebas.
- [x] **8. Crear clases y DAO iniciales.** Se implement├│ el prototipo inicial, separado por responsabilidad.
- [x] **9. Conseguir al menos un INSERT funcional por componente.** La ejecuci├│n local insert├│ Department, Project y WorkRecord, adem├ís de Employee como apoyo; las pruebas tambi├®n verifican las relaciones.
- [x] **10. Registrar problemas pendientes.** Se documentaron en este archivo y en los documentos relacionados.

## Componentes y asignaci├│n propuesta

Los nombres son los indicados por el material de trabajo. Las responsabilidades del negocio deben confirmarse contra el UML original.

| Componente | Responsable principal propuesto | Clase/DAO de referencia | Relaci├│n de referencia |
|---|---|---|---|
| `Department` | Pamela | `Department` / `DepartmentDAO` | Un departamento tiene `0..*` empleados. |
| `Project` | Pamela | `Project` / `ProjectDAO` | Un proyecto tiene `0..*` registros de trabajo. |
| `WorkRecord` | Valentina | `WorkRecord` / `WorkRecordDAO` | Cada registro enlaza un empleado y un proyecto. |
| `Employee` (apoyo) | Compartido para integraci├│n | `Employee` / `EmployeeDAO` | Cada empleado se asocia a un departamento; un empleado tiene `0..*` registros. |

Pamela y Valentina colaboran en UML, integraci├│n, pruebas generales y revisi├│n. La asignaci├│n definitiva requiere acuerdo entre ambas. No se afirma que Valentina tenga permisos de repositorio configurados.

## Relaciones de referencia

- `Department 1 ÔÇö 0..* Employee`.
- `Employee 1 ÔÇö 0..* WorkRecord`.
- `Project 1 ÔÇö 0..* WorkRecord`.

El detalle de atributos, tipos y restricciones est├í en `docs/uml.md` y `docs/database_model.md`, marcado como propuesta.

## Estructura inicial preparada

- `src/domain/`: entidades con validaciones sencillas.
- `src/persistence/`: conexi├│n SQLite, creaci├│n de tablas y DAO de inserci├│n.
- `src/main.py`: demostraci├│n del flujo de inserci├│n.
- `tests/`: pruebas del dominio, esquema, DAO e integridad referencial.

No se agregan `Service`, `Controller`, DAO gen├®rico ni capas adicionales.

## Flujo de ramas propuesto

1. Mantener `main` estable y evitar cambios directos.
2. Desde `main` actualizado, Pamela trabajar├¡a en `feature/pamela-department-project`.
3. Valentina trabajar├¡a en `feature/valentina-work-record`.
4. Integrar mediante `integration/class8` si el equipo mantiene esa estrategia; abrir Pull Requests y solicitar revisi├│n mutua antes de integrar a `main`.
5. Ejecutar las pruebas acordadas antes de completar la integraci├│n.

Las ramas anteriores son nombres propuestos, no est├ín creadas. En esta sesi├│n se contin├║a en `setup/project-structure` por autorizaci├│n de la usuaria; no se hizo commit, push, merge ni Pull Request.

## Bloqueos y decisiones pendientes

1. Conseguir el UML original de la evaluaci├│n anterior y confirmar el modelo con el equipo/docente.
2. Confirmar atributos, m├®todos y reglas de negocio reales; en particular `name`, `work_date` y `hours`.
3. Acordar la distribuci├│n definitiva y el liderazgo de la entidad de apoyo `Employee`.
4. Confirmar acceso y permisos de Valentina al repositorio, sin presumirlos.
5. Confirmar la integraci├│n de ramas cuando el equipo autorice crearlas.
6. Revisar resultados de pruebas e inserciones antes de declarar el taller terminado.
7. Registrar cualquier ajuste al esquema y al motor SQLite en `docs/decisions.md`.
