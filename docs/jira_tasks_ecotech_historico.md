# Tareas propuestas para Jira ÔÇö Taller Clase 8

> Lista preparada para que Valentina la registre en el tablero. No se afirma que se haya accedido a Jira ni que estas tareas ya existan. Las columnas indican una organizaci├│n inicial sugerida, no el estado real de una tarjeta.

## Por hacer

### C8-01 ÔÇö Revisar y validar el UML
- **Descripci├│n:** obtener el UML original de la evaluaci├│n anterior y compararlo con la referencia documentada.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** recibir el UML original y confirmar el caso de negocio.
- **Criterios de aceptaci├│n:** clases, atributos, m├®todos, tipos, relaciones y multiplicidades quedan acordados y documentados; no se atribuye validaci├│n docente sin evidencia.
- **Evidencia esperada:** `docs/uml.md` revisado y decisi├│n del equipo registrada.

### C8-02 ÔÇö Confirmar componentes y responsabilidades
- **Descripci├│n:** acordar `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo, o ajustar seg├║n el UML.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-01.
- **Criterios de aceptaci├│n:** cada componente tiene responsabilidad aprobada y no existen clases agregadas por suposici├│n.
- **Evidencia esperada:** modelo UML y tabla de responsabilidades acordados.

### C8-03 ÔÇö Confirmar distribuci├│n del equipo
- **Descripci├│n:** acordar liderazgo propuesto: Pamela para Department y Project; Valentina para WorkRecord; ambas en integraci├│n.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Media.
- **Dependencias:** C8-02.
- **Criterios de aceptaci├│n:** cada integrante lidera al menos un componente y ambas acuerdan su participaci├│n en integraci├│n.
- **Evidencia esperada:** `docs/team_responsibilities.md` aprobado por ambas.

### C8-04 ÔÇö Confirmar relaciones y multiplicidades
- **Descripci├│n:** validar DepartmentÔÇôEmployee, EmployeeÔÇôWorkRecord y ProjectÔÇôWorkRecord contra el UML original.
- **Responsable:** Valentina (WorkRecord) y Pamela (Department/Project), con revisi├│n mutua.
- **Prioridad:** Alta.
- **Dependencias:** C8-01.
- **Criterios de aceptaci├│n:** las relaciones, obligatoriedad y multiplicidades se reflejan consistentemente en el dominio y esquema.
- **Evidencia esperada:** diagrama actualizado y tabla de relaciones revisada.

### C8-05 ÔÇö Revisar el modelo de base de datos
- **Descripci├│n:** confirmar tablas, tipos, PK, FK, restricciones y el motor SQLite propuesto.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-01 y C8-04.
- **Criterios de aceptaci├│n:** cada columna y restricci├│n tiene justificaci├│n en el UML o requerimiento confirmado.
- **Evidencia esperada:** `docs/database_model.md` acordado.

### C8-06 ÔÇö Crear ramas de trabajo
- **Descripci├│n:** cuando se autorice, crear las ramas propuestas `feature/pamela-department-project`, `feature/valentina-work-record` e `integration/class8`.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Media.
- **Dependencias:** estado Git limpio, confirmaci├│n de permisos y acuerdo de flujo.
- **Criterios de aceptaci├│n:** ramas creadas desde la base acordada; `main` sin cambios directos.
- **Evidencia esperada:** listado de ramas y Pull Requests cuando correspondan.

## En progreso (ubicaci├│n sugerida para registrar trabajo local)

### C8-07 ÔÇö Preparar estructura m├¡nima de dominio y persistencia
- **Descripci├│n:** mantener paquetes sencillos para dominio, SQLite, DAO y pruebas; no agregar `Service` ni `Controller`.
- **Responsable:** Pamela, con revisi├│n de Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-02 y C8-05.
- **Criterios de aceptaci├│n:** estructura clara, sin archivos duplicados ni capas no solicitadas.
- **Evidencia esperada:** inventario de archivos y revisi├│n del equipo.

### C8-08 ÔÇö Implementar clases y DAO iniciales
- **Descripci├│n:** implementar constructores tipados, validaci├│n b├ísica y DAO independientes para las entidades acordadas.
- **Responsable:** Pamela (Department/Project), Valentina (WorkRecord); Employee se coordina como apoyo.
- **Prioridad:** Alta.
- **Dependencias:** C8-02, C8-04 y C8-05.
- **Criterios de aceptaci├│n:** SQL parametrizado solo en persistencia; IDs recuperados; transacciones y conexiones administradas.
- **Evidencia esperada:** pruebas de dominio e inserciones reproducibles.

### C8-09 ÔÇö Verificar inserciones y relaciones
- **Descripci├│n:** probar inserciones para Department, Project, Employee y WorkRecord, incluyendo las claves for├íneas.
- **Responsable:** Valentina (WorkRecord); Pamela (Department/Project); ambas revisan integraci├│n.
- **Prioridad:** Alta.
- **Dependencias:** C8-08.
- **Criterios de aceptaci├│n:** aplicaci├│n y pruebas pasan con base temporal; referencias inexistentes se rechazan.
- **Evidencia esperada:** salida de `python src/main.py` y resultados de `python -m unittest discover -s tests -v`.

## En revisi├│n (ubicaci├│n sugerida)

### C8-10 ÔÇö Revisar documentaci├│n, seguridad y bloqueos
- **Descripci├│n:** revisar README, modelo, estado de Git, exclusiones de archivos locales y asuntos pendientes.
- **Responsable:** Pamela y Valentina, con revisi├│n cruzada.
- **Prioridad:** Media.
- **Dependencias:** C8-01 a C8-09.
- **Criterios de aceptaci├│n:** documentaci├│n coincide con el c├│digo; no hay credenciales; UML no se presenta como validado sin evidencia.
- **Evidencia esperada:** revisi├│n por ambas y lista de pendientes actualizada.

## Terminado

Sin tareas marcadas como terminadas todav├¡a. Mover una tarea aqu├¡ solo despu├®s de cumplir sus criterios de aceptaci├│n y registrar la evidencia; no implica que Jira haya sido actualizado por esta sesi├│n.
