# Tareas propuestas para Jira — Taller Clase 8

> Lista preparada para que Valentina la registre en el tablero. No se afirma que se haya accedido a Jira ni que estas tareas ya existan. Las columnas indican una organización inicial sugerida, no el estado real de una tarjeta.

## Por hacer

### C8-01 — Revisar y validar el UML
- **Descripción:** obtener el UML original de la evaluación anterior y compararlo con la referencia documentada.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** recibir el UML original y confirmar el caso de negocio.
- **Criterios de aceptación:** clases, atributos, métodos, tipos, relaciones y multiplicidades quedan acordados y documentados; no se atribuye validación docente sin evidencia.
- **Evidencia esperada:** `docs/uml.md` revisado y decisión del equipo registrada.

### C8-02 — Confirmar componentes y responsabilidades
- **Descripción:** acordar `Department`, `Project` y `WorkRecord`, con `Employee` como entidad de apoyo, o ajustar según el UML.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-01.
- **Criterios de aceptación:** cada componente tiene responsabilidad aprobada y no existen clases agregadas por suposición.
- **Evidencia esperada:** modelo UML y tabla de responsabilidades acordados.

### C8-03 — Confirmar distribución del equipo
- **Descripción:** acordar liderazgo propuesto: Pamela para Department y Project; Valentina para WorkRecord; ambas en integración.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Media.
- **Dependencias:** C8-02.
- **Criterios de aceptación:** cada integrante lidera al menos un componente y ambas acuerdan su participación en integración.
- **Evidencia esperada:** `docs/team_responsibilities.md` aprobado por ambas.

### C8-04 — Confirmar relaciones y multiplicidades
- **Descripción:** validar Department–Employee, Employee–WorkRecord y Project–WorkRecord contra el UML original.
- **Responsable:** Valentina (WorkRecord) y Pamela (Department/Project), con revisión mutua.
- **Prioridad:** Alta.
- **Dependencias:** C8-01.
- **Criterios de aceptación:** las relaciones, obligatoriedad y multiplicidades se reflejan consistentemente en el dominio y esquema.
- **Evidencia esperada:** diagrama actualizado y tabla de relaciones revisada.

### C8-05 — Revisar el modelo de base de datos
- **Descripción:** confirmar tablas, tipos, PK, FK, restricciones y el motor SQLite propuesto.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-01 y C8-04.
- **Criterios de aceptación:** cada columna y restricción tiene justificación en el UML o requerimiento confirmado.
- **Evidencia esperada:** `docs/database_model.md` acordado.

### C8-06 — Crear ramas de trabajo
- **Descripción:** cuando se autorice, crear las ramas propuestas `feature/pamela-department-project`, `feature/valentina-work-record` e `integration/class8`.
- **Responsable:** Pamela y Valentina.
- **Prioridad:** Media.
- **Dependencias:** estado Git limpio, confirmación de permisos y acuerdo de flujo.
- **Criterios de aceptación:** ramas creadas desde la base acordada; `main` sin cambios directos.
- **Evidencia esperada:** listado de ramas y Pull Requests cuando correspondan.

## En progreso (ubicación sugerida para registrar trabajo local)

### C8-07 — Preparar estructura mínima de dominio y persistencia
- **Descripción:** mantener paquetes sencillos para dominio, SQLite, DAO y pruebas; no agregar `Service` ni `Controller`.
- **Responsable:** Pamela, con revisión de Valentina.
- **Prioridad:** Alta.
- **Dependencias:** C8-02 y C8-05.
- **Criterios de aceptación:** estructura clara, sin archivos duplicados ni capas no solicitadas.
- **Evidencia esperada:** inventario de archivos y revisión del equipo.

### C8-08 — Implementar clases y DAO iniciales
- **Descripción:** implementar constructores tipados, validación básica y DAO independientes para las entidades acordadas.
- **Responsable:** Pamela (Department/Project), Valentina (WorkRecord); Employee se coordina como apoyo.
- **Prioridad:** Alta.
- **Dependencias:** C8-02, C8-04 y C8-05.
- **Criterios de aceptación:** SQL parametrizado solo en persistencia; IDs recuperados; transacciones y conexiones administradas.
- **Evidencia esperada:** pruebas de dominio e inserciones reproducibles.

### C8-09 — Verificar inserciones y relaciones
- **Descripción:** probar inserciones para Department, Project, Employee y WorkRecord, incluyendo las claves foráneas.
- **Responsable:** Valentina (WorkRecord); Pamela (Department/Project); ambas revisan integración.
- **Prioridad:** Alta.
- **Dependencias:** C8-08.
- **Criterios de aceptación:** aplicación y pruebas pasan con base temporal; referencias inexistentes se rechazan.
- **Evidencia esperada:** salida de `python src/main.py` y resultados de `python -m unittest discover -s tests -v`.

## En revisión (ubicación sugerida)

### C8-10 — Revisar documentación, seguridad y bloqueos
- **Descripción:** revisar README, modelo, estado de Git, exclusiones de archivos locales y asuntos pendientes.
- **Responsable:** Pamela y Valentina, con revisión cruzada.
- **Prioridad:** Media.
- **Dependencias:** C8-01 a C8-09.
- **Criterios de aceptación:** documentación coincide con el código; no hay credenciales; UML no se presenta como validado sin evidencia.
- **Evidencia esperada:** revisión por ambas y lista de pendientes actualizada.

## Terminado

Sin tareas marcadas como terminadas todavía. Mover una tarea aquí solo después de cumplir sus criterios de aceptación y registrar la evidencia; no implica que Jira haya sido actualizado por esta sesión.
