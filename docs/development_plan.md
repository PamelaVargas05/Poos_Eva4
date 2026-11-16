# Plan de desarrollo

Integrantes: Pamela (P) y Valentina (V). Los responsables son **sugeridos**; deben acordarse entre ambas.

## 1. Tablero Kanban en Jira
Columnas: **Por hacer** → **En progreso** → **En revisión** → **Hecho**.

Reglas sugeridas:
- Máximo 2 tarjetas en "En progreso" por persona.
- Toda tarjeta pasa por "En revisión" con revisión de la otra integrante.
- Una tarjeta está "Hecha" cuando cumple sus criterios de aceptación y está fusionada a `main` mediante Pull Request.

## 2. Etapas
1. Preparación y análisis
2. Diseño (UML)
3. Programación del dominio
4. Base de datos
5. CRUD
6. Seguridad y excepciones
7. Pruebas
8. Documentación y cierre

## 3. Tarjetas propuestas
| ID | Grupo | Tarjeta | Responsable sugerido | Descripción | Criterios de aceptación |
|----|-------|---------|----------------------|-------------|-------------------------|
| T-01 | Preparación | Configurar repositorio y estructura base | P | Revisar la rama `setup/project-structure` y fusionarla. | Estructura creada, `python src/main.py` funciona. |
| T-02 | Preparación | Configurar tablero Jira | V | Crear tablero Kanban con 4 columnas e importar tarjetas. | Tablero visible para ambas. |
| T-03 | Análisis | Confirmar caso de negocio | P y V | Acordar alcance con el enunciado. | `requirements.md` sin pendientes críticos. |
| T-04 | Análisis | Redactar historias de usuario | V | Completar HU y criterios. | Cada HU con criterios verificables. |
| T-05 | Diseño | Elaborar UML de clases | P | Clases, atributos, métodos, relaciones. | `uml.md` completo y validado. |
| T-06 | Diseño | Validar UML con el docente | P y V | Corregir observaciones. | UML aprobado. |
| T-07 | Programación | Implementar clases del dominio | P | Código fiel al UML, con encapsulamiento. | Clases coinciden con UML. |
| T-08 | Programación | Implementar relaciones/herencia | V | Solo las del UML. | Relaciones funcionan según multiplicidades. |
| T-09 | Base de datos | Decidir SQLite o MySQL | P y V | Registrar en `decisions.md`. | Decisión documentada. |
| T-10 | Base de datos | Diseñar tablas (nombres en inglés) | V | Modelo relacional coherente con UML. | Script de creación revisado. |
| T-11 | Base de datos | Implementar conexión y acceso a datos | P | Consultas parametrizadas. | Conexión funciona; sin credenciales en el repo. |
| T-12 | CRUD | Crear (Create) | P | Insertar entidades con validación. | Registro guardado o error claro. |
| T-13 | CRUD | Consultar (Read) | V | Listar y buscar. | Datos mostrados correctamente. |
| T-14 | CRUD | Actualizar (Update) | P | Modificar con validación. | Cambios persistentes. |
| T-15 | CRUD | Eliminar (Delete) | V | Eliminar con confirmación. | Registro eliminado. |
| T-16 | Seguridad | Validación de entradas | V | Validar tipos, rangos y formatos. | Entradas inválidas rechazadas. |
| T-17 | Seguridad | Manejo de excepciones | P | Capturar errores y mostrar mensajes en español. | Sin trazas internas al usuario. |
| T-18 | Seguridad | Revisión de secretos y `.gitignore` | V | Verificar que no haya credenciales. | Sin archivos sensibles en Git. |
| T-19 | Pruebas | Pruebas de dominio | P | Casos válidos e inválidos. | Pruebas pasan. |
| T-20 | Pruebas | Pruebas de CRUD | V | Probar con base temporal. | Pruebas pasan. |
| T-21 | Documentación | Actualizar README y docs | P y V | Reflejar el estado real. | Docs coherentes con el código. |
| T-22 | Documentación | Preparar entrega final | P y V | Revisión general y demo. | Todo en `main`, tablero en "Hecho". |
