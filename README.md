# Viaje de Aventura —

## Descripción
Prototipo académico en Python para practicar Programación Orientada a Objetos Seguros mediante un sistema de gestión de departamentos, proyectos y registros de tiempo de EcoTech Solutions. El modelo implementado es una referencia de trabajo basada en el material del taller; no reemplaza ni afirma ser el UML original validado.

## Objetivo
Completar los requisitos de Clase 1 y Clase 2 de Programación Orientada a Objetos Seguros, con clases de dominio encapsuladas, relaciones controladas, persistencia SQLite y pruebas automatizadas. El modelo sigue sujeto a revisión contra el UML original.

## Tecnologías
- Python 3.10 o superior
- SQLite mediante `sqlite3` (biblioteca estándar)
- Git y GitHub (control de versiones)
- Jira, tablero Kanban (gestión ágil)

## Componentes y relaciones de referencia

- `Department`: departamento; se relaciona con cero o más empleados.
- `Project`: proyecto; se relaciona con cero o más registros de trabajo.
- `WorkRecord`: registra fecha y horas y enlaza un empleado con un proyecto.
- `Employee`: entidad de apoyo; cada empleado se asocia a un departamento y puede tener cero o más registros.

Multiplicidades propuestas: `Department 1 — 0..* Employee`, `Employee 1 — 0..* WorkRecord` y `Project 1 — 0..* WorkRecord`. Atributos, tipos y reglas de negocio aún requieren validación contra el UML original.

Las clases almacenan sus atributos de forma privada y ofrecen propiedades de solo lectura. Los métodos públicos validan las modificaciones y controlan asociaciones; las consultas de empleados y registros devuelven tuplas, no las listas internas.

## Estructura de carpetas
```
Poos_Eva4/
├── docs/                    Documentación del proyecto (en español)
│   ├── UML_base_v1.md        Referencia inicial, no UML original
│   ├── uml.md                Modelo de referencia por validar
│   ├── uml_review.md
│   ├── database_model.md
│   ├── team_responsibilities.md
│   ├── class8_implementation_plan.md
│   ├── project_walkthrough.md
│   ├── jira_tasks.md
│   ├── requirements.md
│   ├── architecture.md
│   ├── development_plan.md
│   └── decisions.md
├── src/                     Código fuente (en inglés)
│   ├── __init__.py
│   ├── domain/              Entidades y validación básica
│   │   ├── __init__.py
│   │   ├── department.py
│   │   ├── employee.py
│   │   ├── project.py
│   │   └── work_record.py
│   ├── persistence/         Conexión SQLite, esquema y DAO
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── create_db.py
│   │   ├── department_dao.py
│   │   ├── employee_dao.py
│   │   ├── project_dao.py
│   │   └── work_record_dao.py
│   └── main.py              Demostración de inserciones
├── tests/                   Pruebas automatizadas con unittest
│   ├── README.md
│   ├── test_domain.py
│   └── test_persistence.py
├── data/                    Base local generada, ignorada por Git
│   └── ecotech.db
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación y ejecución

Se requiere Python 3.10 o superior. Desde la raíz del repositorio, en Windows PowerShell:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si la política de ejecución bloquea el script, revisar la configuración de PowerShell del equipo; no es necesario instalar paquetes externos para este prototipo.

Ejecutar la demostración:

```
python src/main.py
```

Ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

La demostración crea `data/ecotech.db`, inicializa las tablas e inserta datos ficticios. El archivo de base de datos local está excluido por `.gitignore`.

En la última validación local, `python src/main.py` completó las cuatro inserciones de demostración y las cinco pruebas de `unittest` finalizaron correctamente. Esto verifica el prototipo actual, no la aprobación del UML.

## Responsabilidades propuestas

| Integrante | Componentes | Colaboración |
|---|---|---|
| Pamela | `Department`, `Project` | Integración y revisión del repositorio. |
| Valentina | `WorkRecord` | Revisar sus relaciones con `Employee` y `Project`, pruebas y organización de tareas Kanban. |
| Ambas | UML e integración | Pruebas generales, Pull Requests y documentación. |

La distribución es propuesta y debe ser acordada por el equipo. No se afirma que Valentina tenga permisos de repositorio configurados.

## Estado y problemas pendientes

- Existe una implementación inicial de dominio y persistencia SQLite para los cuatro nombres de clase de referencia.
- `docs/UML_base_v1.md` es una referencia creada desde el material compartido, **no** el UML original ni una validación docente.
- Deben confirmarse con el equipo el UML, los atributos, tipos, reglas de negocio y multiplicidades definitivas.
- El equipo debe revisar los resultados de pruebas e inserciones antes de considerar terminado el taller.
- La creación de ramas quedó pendiente; esta sesión continúa en `setup/project-structure` por indicación de la usuaria.
- Debe confirmarse el acceso de Valentina al repositorio antes de asignar revisiones o ramas.
- Las tarjetas de `docs/jira_tasks.md` están preparadas como propuesta; no se afirma que se hayan creado en Jira.

## Guía para comprender el proyecto

Para recorrer el flujo completo con ejemplos, consulta la [guía paso a paso](docs/project_walkthrough.md).

### Qué contiene cada carpeta

- `docs/`: explica el modelo de referencia, el esquema de datos, la planificación y los pendientes.
- `src/domain/`: clases que representan los datos del negocio y validan valores básicos; no ejecutan SQL.
- `src/persistence/`: abre la conexión SQLite, crea las tablas y ejecuta los `INSERT` parametrizados mediante DAO.
- `tests/`: pruebas automáticas de las clases, las tablas, las inserciones y las claves foráneas.
- `data/`: contiene `ecotech.db`, creado al ejecutar el programa. La base local está excluida por `.gitignore`.
- `__pycache__/` y `.venv/` son artefactos/entorno locales ignorados por Git; no forman parte del código fuente.

### Clases del dominio

| Clase | Para qué sirve |
|---|---|
| `Department` | Representa un departamento y valida su nombre e identificador opcional. |
| `Employee` | Representa el empleado de apoyo y requiere el identificador de su departamento. |
| `Project` | Representa un proyecto y valida su nombre e identificador opcional. |
| `WorkRecord` | Registra empleado, proyecto, fecha y horas; valida referencias positivas, fecha y horas mayores que cero. |

Estos atributos son los del prototipo de referencia; deben confirmarse contra el UML original.

### DAO y SQLite

Cada DAO se ocupa de insertar una entidad en su tabla y devuelve el ID generado:

| DAO | Tabla | Uso |
|---|---|---|
| `DepartmentDAO` | `departments` | Inserta departamentos. |
| `EmployeeDAO` | `employees` | Inserta empleados vinculados a un departamento. |
| `ProjectDAO` | `projects` | Inserta proyectos. |
| `WorkRecordDAO` | `work_records` | Inserta registros vinculados a empleado y proyecto. |

`connection.py` crea un objeto `sqlite3.Connection` y activa la validación de claves foráneas. `main.py` pasa esa misma conexión a la creación del esquema y a los DAO. Cada DAO usa parámetros SQL (`?`) y no concatena los datos en la consulta. `create_db.py` define las cuatro tablas y sus claves foráneas.

### Qué ocurre al ejecutar `main.py`

Al ejecutar `python src/main.py`, el programa abre o crea `data/ecotech.db`, crea las tablas si aún no existen, construye objetos ficticios, inserta Department, Employee, Project y WorkRecord en ese orden, muestra los IDs y cierra la conexión. Cada ejecución agrega una nueva serie de registros de demostración.

### Pruebas

Desde la raíz del proyecto:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas usan SQLite en memoria; comprueban validaciones, las cuatro tablas, una secuencia de inserciones y el rechazo de claves foráneas inexistentes.

### Responsabilidades propuestas

| Integrante | Liderazgo propuesto | Colaboración |
|---|---|---|
| Pamela | `Department` y `Project` | Integración y revisión del repositorio. |
| Valentina | `WorkRecord` | Revisar vínculos con `Employee` y `Project`, pruebas y organización Kanban. |
| Ambas | — | Revisar el UML, integrar, probar y revisar cambios. |

La distribución es una propuesta para acordar; no confirma permisos de repositorio ni tareas registradas en Jira.

### Documentos de la actividad y complementarios

Según las actividades y entregables compartidos para Clase 8, los elementos centrales son el repositorio con estructura/código, `docs/uml.md` como UML actualizado, la distribución de responsabilidades, el diseño de tablas y el estado del proyecto en este README. El plan de implementación registra el avance y los bloqueos.

Como apoyo complementario están `docs/UML_base_v1.md` (referencia inicial, no UML original), `docs/uml_review.md`, `docs/architecture.md`, `docs/requirements.md`, `docs/decisions.md`, `docs/development_plan.md`, `docs/jira_tasks.md` y esta guía ampliada. La clasificación resume el material del taller compartido; el equipo debe confirmar cualquier pauta formal del docente.

## Flujo de trabajo con GitHub
- No se trabaja directamente sobre `main`.
- Cada tarjeta de Jira se desarrolla en una rama propia, por ejemplo `feature/<short-name>`.
- Commits pequeños, con mensajes claros.
- Se abre un Pull Request y la otra integrante lo revisa antes de fusionarlo a `main`.
- Nunca se suben credenciales, archivos `.env` ni bases de datos (`*.db`).

## Integrantes
- Pamela
- Valentina
