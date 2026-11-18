# Modelo inicial de base de datos

> Este esquema SQLite es un prototipo basado en las relaciones de referencia compartidas para el taller. El UML original no está disponible; los atributos y restricciones deben confirmarse antes de considerar el diseño definitivo.

## Tablas propuestas

### `departments`

| Columna | Tipo SQLite | Restricciones |
|---|---|---|
| `department_id` | `INTEGER` | Clave primaria; autoincremental. |
| `name` | `TEXT` | `NOT NULL`. |

### `employees`

| Columna | Tipo SQLite | Restricciones |
|---|---|---|
| `employee_id` | `INTEGER` | Clave primaria; autoincremental. |
| `name` | `TEXT` | `NOT NULL`. |
| `department_id` | `INTEGER` | `NOT NULL`; FK a `departments.department_id`. |

### `projects`

| Columna | Tipo SQLite | Restricciones |
|---|---|---|
| `project_id` | `INTEGER` | Clave primaria; autoincremental. |
| `name` | `TEXT` | `NOT NULL`. |

### `work_records`

| Columna | Tipo SQLite | Restricciones |
|---|---|---|
| `work_record_id` | `INTEGER` | Clave primaria; autoincremental. |
| `employee_id` | `INTEGER` | `NOT NULL`; FK a `employees.employee_id`. |
| `project_id` | `INTEGER` | `NOT NULL`; FK a `projects.project_id`. |
| `work_date` | `TEXT` | `NOT NULL`; fecha ISO 8601 en el prototipo. |
| `hours` | `REAL` | `NOT NULL`; `CHECK (hours > 0)`. |

## Relaciones y justificación de claves foráneas

| Tabla dependiente | Clave foránea | Referencia | Relación de referencia |
|---|---|---|---|
| `employees` | `department_id` | `departments.department_id` | Un departamento puede tener cero o muchos empleados; cada empleado apunta a un departamento. |
| `work_records` | `employee_id` | `employees.employee_id` | Un empleado puede tener cero o muchos registros; cada registro apunta a un empleado. |
| `work_records` | `project_id` | `projects.project_id` | Un proyecto puede tener cero o muchos registros; cada registro apunta a un proyecto. |

Las claves foráneas mantienen la integridad de las asociaciones. SQLite debe tener habilitado `PRAGMA foreign_keys = ON` para cada conexión.

## Decisiones pendientes

- Confirmar con el UML y el equipo cada tabla, columna, tipo y cardinalidad.
- Confirmar si el empleado tiene un único departamento y si ambas referencias de `work_records` son obligatorias.
- Revisar si hacen falta más datos o restricciones según el caso de negocio.
- La elección de SQLite es la decisión usada por este prototipo del taller; registrar cualquier cambio futuro en `docs/decisions.md`.
