# Plan de desarrollo

Integrantes: Pamela (P) y Valentina (V). Los responsables son **sugeridos**; deben acordarse entre ambas.

## 1. Tablero Kanban en Jira
Columnas: **Por hacer** ÔåÆ **En progreso** ÔåÆ **En revisi├│n** ÔåÆ **Hecho**.

Reglas sugeridas:
- M├íximo 2 tarjetas en "En progreso" por persona.
- Toda tarjeta pasa por "En revisi├│n" con revisi├│n de la otra integrante.
- Una tarjeta est├í "Hecha" cuando cumple sus criterios de aceptaci├│n y est├í fusionada a `main` mediante Pull Request.

## 2. Etapas
1. Preparaci├│n y an├ílisis
2. Dise├▒o (UML)
3. Programaci├│n del dominio
4. Base de datos
5. CRUD
6. Seguridad y excepciones
7. Pruebas
8. Documentaci├│n y cierre

## 3. Tarjetas propuestas
| ID | Grupo | Tarjeta | Responsable sugerido | Descripci├│n | Criterios de aceptaci├│n |
|----|-------|---------|----------------------|-------------|-------------------------|
| T-01 | Preparaci├│n | Configurar repositorio y estructura base | P | Revisar la rama `setup/project-structure` y fusionarla. | Estructura creada, `python src/main.py` funciona. |
| T-02 | Preparaci├│n | Configurar tablero Jira | V | Crear tablero Kanban con 4 columnas e importar tarjetas. | Tablero visible para ambas. |
| T-03 | An├ílisis | Confirmar caso de negocio | P y V | Acordar alcance con el enunciado. | `requirements.md` sin pendientes cr├¡ticos. |
| T-04 | An├ílisis | Redactar historias de usuario | V | Completar HU y criterios. | Cada HU con criterios verificables. |
| T-05 | Dise├▒o | Elaborar UML de clases | P | Clases, atributos, m├®todos, relaciones. | `uml.md` completo y validado. |
| T-06 | Dise├▒o | Validar UML con el docente | P y V | Corregir observaciones. | UML aprobado. |
| T-07 | Programaci├│n | Implementar clases del dominio | P | C├│digo fiel al UML, con encapsulamiento. | Clases coinciden con UML. |
| T-08 | Programaci├│n | Implementar relaciones/herencia | V | Solo las del UML. | Relaciones funcionan seg├║n multiplicidades. |
| T-09 | Base de datos | Decidir SQLite o MySQL | P y V | Registrar en `decisions.md`. | Decisi├│n documentada. |
| T-10 | Base de datos | Dise├▒ar tablas (nombres en ingl├®s) | V | Modelo relacional coherente con UML. | Script de creaci├│n revisado. |
| T-11 | Base de datos | Implementar conexi├│n y acceso a datos | P | Consultas parametrizadas. | Conexi├│n funciona; sin credenciales en el repo. |
| T-12 | CRUD | Crear (Create) | P | Insertar entidades con validaci├│n. | Registro guardado o error claro. |
| T-13 | CRUD | Consultar (Read) | V | Listar y buscar. | Datos mostrados correctamente. |
| T-14 | CRUD | Actualizar (Update) | P | Modificar con validaci├│n. | Cambios persistentes. |
| T-15 | CRUD | Eliminar (Delete) | V | Eliminar con confirmaci├│n. | Registro eliminado. |
| T-16 | Seguridad | Validaci├│n de entradas | V | Validar tipos, rangos y formatos. | Entradas inv├ílidas rechazadas. |
| T-17 | Seguridad | Manejo de excepciones | P | Capturar errores y mostrar mensajes en espa├▒ol. | Sin trazas internas al usuario. |
| T-18 | Seguridad | Revisi├│n de secretos y `.gitignore` | V | Verificar que no haya credenciales. | Sin archivos sensibles en Git. |
| T-19 | Pruebas | Pruebas de dominio | P | Casos v├ílidos e inv├ílidos. | Pruebas pasan. |
| T-20 | Pruebas | Pruebas de CRUD | V | Probar con base temporal. | Pruebas pasan. |
| T-21 | Documentaci├│n | Actualizar README y docs | P y V | Reflejar el estado real. | Docs coherentes con el c├│digo. |
| T-22 | Documentaci├│n | Preparar entrega final | P y V | Revisi├│n general y demo. | Todo en `main`, tablero en "Hecho". |

## 4. Flujo de ramas propuesto para Clase 8

El material del taller propone `feature/pamela-department-project`, `feature/valentina-work-record` e `integration/class8`. Son nombres propuestos y no se afirma que existan.

1. Confirmar con el equipo el estado del repositorio y los permisos.
2. Crear ramas desde `main` actualizado, sin trabajar directamente sobre `main`.
3. Abrir Pull Requests hacia la rama de integraci├│n acordada y solicitar revisi├│n mutua.
4. Ejecutar las pruebas antes de integrar a `main` mediante Pull Request.

En esta sesi├│n se continu├│ en `setup/project-structure` por indicaci├│n de la usuaria; no se crearon ramas, no se modific├│ `main`, y no se hizo commit, push ni merge.
