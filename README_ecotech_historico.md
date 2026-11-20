# Viaje de Aventura ÔÇö

## Descripci├│n
Prototipo acad├®mico en Python para practicar Programaci├│n Orientada a Objetos Seguros mediante un sistema de gesti├│n de departamentos, proyectos y registros de tiempo de EcoTech Solutions. El modelo implementado es una referencia de trabajo basada en el material del taller; no reemplaza ni afirma ser el UML original validado.

## Objetivo
Completar los requisitos de Clase 1 y Clase 2 de Programaci├│n Orientada a Objetos Seguros, con clases de dominio encapsuladas, relaciones controladas, persistencia SQLite y pruebas automatizadas. El modelo sigue sujeto a revisi├│n contra el UML original.

## Tecnolog├¡as
- Python 3.10 o superior
- SQLite mediante `sqlite3` (biblioteca est├índar)
- Git y GitHub (control de versiones)
- Jira, tablero Kanban (gesti├│n ├ígil)

## Componentes y relaciones de referencia

- `Department`: departamento; se relaciona con cero o m├ís empleados.
- `Project`: proyecto; se relaciona con cero o m├ís registros de trabajo.
- `WorkRecord`: registra fecha y horas y enlaza un empleado con un proyecto.
- `Employee`: entidad de apoyo; cada empleado se asocia a un departamento y puede tener cero o m├ís registros.

Multiplicidades propuestas: `Department 1 ÔÇö 0..* Employee`, `Employee 1 ÔÇö 0..* WorkRecord` y `Project 1 ÔÇö 0..* WorkRecord`. Atributos, tipos y reglas de negocio a├║n requieren validaci├│n contra el UML original.

Las clases almacenan sus atributos de forma privada y ofrecen propiedades de solo lectura. Los m├®todos p├║blicos validan las modificaciones y controlan asociaciones; las consultas de empleados y registros devuelven tuplas, no las listas internas.

## Estructura de carpetas
```
Poos_Eva4/
Ôö£ÔöÇÔöÇ docs/                    Documentaci├│n del proyecto (en espa├▒ol)
Ôöé   Ôö£ÔöÇÔöÇ UML_base_v1.md        Referencia inicial, no UML original
Ôöé   Ôö£ÔöÇÔöÇ uml.md                Modelo de referencia por validar
Ôöé   Ôö£ÔöÇÔöÇ uml_review.md
Ôöé   Ôö£ÔöÇÔöÇ database_model.md
Ôöé   Ôö£ÔöÇÔöÇ team_responsibilities.md
Ôöé   Ôö£ÔöÇÔöÇ class8_implementation_plan.md
Ôöé   Ôö£ÔöÇÔöÇ project_walkthrough.md
Ôöé   Ôö£ÔöÇÔöÇ jira_tasks.md
Ôöé   Ôö£ÔöÇÔöÇ requirements.md
Ôöé   Ôö£ÔöÇÔöÇ architecture.md
Ôöé   Ôö£ÔöÇÔöÇ development_plan.md
Ôöé   ÔööÔöÇÔöÇ decisions.md
Ôö£ÔöÇÔöÇ src/                     C├│digo fuente (en ingl├®s)
Ôöé   Ôö£ÔöÇÔöÇ __init__.py
Ôöé   Ôö£ÔöÇÔöÇ domain/              Entidades y validaci├│n b├ísica
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ __init__.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ department.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ employee.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ project.py
Ôöé   Ôöé   ÔööÔöÇÔöÇ work_record.py
Ôöé   Ôö£ÔöÇÔöÇ persistence/         Conexi├│n SQLite, esquema y DAO
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ __init__.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ connection.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ create_db.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ department_dao.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ employee_dao.py
Ôöé   Ôöé   Ôö£ÔöÇÔöÇ project_dao.py
Ôöé   Ôöé   ÔööÔöÇÔöÇ work_record_dao.py
Ôöé   ÔööÔöÇÔöÇ main.py              Demostraci├│n de inserciones
Ôö£ÔöÇÔöÇ tests/                   Pruebas automatizadas con unittest
Ôöé   Ôö£ÔöÇÔöÇ README.md
Ôöé   Ôö£ÔöÇÔöÇ test_domain.py
Ôöé   ÔööÔöÇÔöÇ test_persistence.py
Ôö£ÔöÇÔöÇ data/                    Base local generada, ignorada por Git
Ôöé   ÔööÔöÇÔöÇ ecotech.db
Ôö£ÔöÇÔöÇ .gitignore
Ôö£ÔöÇÔöÇ README.md
ÔööÔöÇÔöÇ requirements.txt
```

## Instalaci├│n y ejecuci├│n

Se requiere Python 3.10 o superior. Desde la ra├¡z del repositorio, en Windows PowerShell:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si la pol├¡tica de ejecuci├│n bloquea el script, revisar la configuraci├│n de PowerShell del equipo; no es necesario instalar paquetes externos para este prototipo.

Ejecutar la demostraci├│n:

```
python src/main.py
```

Ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

La demostraci├│n crea `data/ecotech.db`, inicializa las tablas e inserta datos ficticios. El archivo de base de datos local est├í excluido por `.gitignore`.

En la ├║ltima validaci├│n local, `python src/main.py` complet├│ las cuatro inserciones de demostraci├│n y las cinco pruebas de `unittest` finalizaron correctamente. Esto verifica el prototipo actual, no la aprobaci├│n del UML.

## Responsabilidades propuestas

| Integrante | Componentes | Colaboraci├│n |
|---|---|---|
| Pamela | `Department`, `Project` | Integraci├│n y revisi├│n del repositorio. |
| Valentina | `WorkRecord` | Revisar sus relaciones con `Employee` y `Project`, pruebas y organizaci├│n de tareas Kanban. |
| Ambas | UML e integraci├│n | Pruebas generales, Pull Requests y documentaci├│n. |

La distribuci├│n es propuesta y debe ser acordada por el equipo. No se afirma que Valentina tenga permisos de repositorio configurados.

## Estado y problemas pendientes

- Existe una implementaci├│n inicial de dominio y persistencia SQLite para los cuatro nombres de clase de referencia.
- `docs/UML_base_v1.md` es una referencia creada desde el material compartido, **no** el UML original ni una validaci├│n docente.
- Deben confirmarse con el equipo el UML, los atributos, tipos, reglas de negocio y multiplicidades definitivas.
- El equipo debe revisar los resultados de pruebas e inserciones antes de considerar terminado el taller.
- La creaci├│n de ramas qued├│ pendiente; esta sesi├│n contin├║a en `setup/project-structure` por indicaci├│n de la usuaria.
- Debe confirmarse el acceso de Valentina al repositorio antes de asignar revisiones o ramas.
- Las tarjetas de `docs/jira_tasks.md` est├ín preparadas como propuesta; no se afirma que se hayan creado en Jira.

## Gu├¡a para comprender el proyecto

Para recorrer el flujo completo con ejemplos, consulta la [gu├¡a paso a paso](docs/project_walkthrough.md).

### Qu├® contiene cada carpeta

- `docs/`: explica el modelo de referencia, el esquema de datos, la planificaci├│n y los pendientes.
- `src/domain/`: clases que representan los datos del negocio y validan valores b├ísicos; no ejecutan SQL.
- `src/persistence/`: abre la conexi├│n SQLite, crea las tablas y ejecuta los `INSERT` parametrizados mediante DAO.
- `tests/`: pruebas autom├íticas de las clases, las tablas, las inserciones y las claves for├íneas.
- `data/`: contiene `ecotech.db`, creado al ejecutar el programa. La base local est├í excluida por `.gitignore`.
- `__pycache__/` y `.venv/` son artefactos/entorno locales ignorados por Git; no forman parte del c├│digo fuente.

### Clases del dominio

| Clase | Para qu├® sirve |
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

`connection.py` crea un objeto `sqlite3.Connection` y activa la validaci├│n de claves for├íneas. `main.py` pasa esa misma conexi├│n a la creaci├│n del esquema y a los DAO. Cada DAO usa par├ímetros SQL (`?`) y no concatena los datos en la consulta. `create_db.py` define las cuatro tablas y sus claves for├íneas.

### Qu├® ocurre al ejecutar `main.py`

Al ejecutar `python src/main.py`, el programa abre o crea `data/ecotech.db`, crea las tablas si a├║n no existen, construye objetos ficticios, inserta Department, Employee, Project y WorkRecord en ese orden, muestra los IDs y cierra la conexi├│n. Cada ejecuci├│n agrega una nueva serie de registros de demostraci├│n.

### Pruebas

Desde la ra├¡z del proyecto:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas usan SQLite en memoria; comprueban validaciones, las cuatro tablas, una secuencia de inserciones y el rechazo de claves for├íneas inexistentes.

### Responsabilidades propuestas

| Integrante | Liderazgo propuesto | Colaboraci├│n |
|---|---|---|
| Pamela | `Department` y `Project` | Integraci├│n y revisi├│n del repositorio. |
| Valentina | `WorkRecord` | Revisar v├¡nculos con `Employee` y `Project`, pruebas y organizaci├│n Kanban. |
| Ambas | ÔÇö | Revisar el UML, integrar, probar y revisar cambios. |

La distribuci├│n es una propuesta para acordar; no confirma permisos de repositorio ni tareas registradas en Jira.

### Documentos de la actividad y complementarios

Seg├║n las actividades y entregables compartidos para Clase 8, los elementos centrales son el repositorio con estructura/c├│digo, `docs/uml.md` como UML actualizado, la distribuci├│n de responsabilidades, el dise├▒o de tablas y el estado del proyecto en este README. El plan de implementaci├│n registra el avance y los bloqueos.

Como apoyo complementario est├ín `docs/UML_base_v1.md` (referencia inicial, no UML original), `docs/uml_review.md`, `docs/architecture.md`, `docs/requirements.md`, `docs/decisions.md`, `docs/development_plan.md`, `docs/jira_tasks.md` y esta gu├¡a ampliada. La clasificaci├│n resume el material del taller compartido; el equipo debe confirmar cualquier pauta formal del docente.

## Flujo de trabajo con GitHub
- No se trabaja directamente sobre `main`.
- Cada tarjeta de Jira se desarrolla en una rama propia, por ejemplo `feature/<short-name>`.
- Commits peque├▒os, con mensajes claros.
- Se abre un Pull Request y la otra integrante lo revisa antes de fusionarlo a `main`.
- Nunca se suben credenciales, archivos `.env` ni bases de datos (`*.db`).

## Integrantes
- Pamela
- Valentina
