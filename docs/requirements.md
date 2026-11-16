# Requerimientos

> Este documento se completará con el caso de negocio confirmado. Los datos sin confirmar están marcados como **[PENDIENTE]**.

## 1. Requerimientos funcionales
| ID | Descripción | Prioridad | Estado |
|----|-------------|-----------|--------|
| RF-01 | Registrar (crear) las entidades principales del sistema. **[PENDIENTE: definir entidades según UML]** | Alta | Por confirmar |
| RF-02 | Consultar (leer) las entidades registradas. | Alta | Por confirmar |
| RF-03 | Actualizar los datos de las entidades registradas. | Alta | Por confirmar |
| RF-04 | Eliminar entidades registradas. | Media | Por confirmar |
| RF-05 | Guardar la información en una base de datos (SQLite o MySQL). | Alta | Por confirmar |
| RF-06 | Validar los datos ingresados y mostrar mensajes de error en español. | Alta | Por confirmar |
| RF-07 | **[PENDIENTE]** Otros requerimientos del caso de negocio. | - | - |

Los RF-01 a RF-06 se derivan de los objetivos académicos (CRUD, base de datos, excepciones) y deben ajustarse al caso real.

## 2. Requerimientos no funcionales
| ID | Descripción | Prioridad |
|----|-------------|-----------|
| RNF-01 | Código, tablas y columnas en inglés; documentación y mensajes al usuario en español. | Alta |
| RNF-02 | Encapsulamiento de atributos y separación de responsabilidades. | Alta |
| RNF-03 | Manejo de excepciones controlado, sin exponer detalles internos al usuario. | Alta |
| RNF-04 | Seguridad: sin credenciales en el repositorio; validación de entradas; consultas SQL parametrizadas. | Alta |
| RNF-05 | Coherencia entre el UML validado y el código. | Alta |
| RNF-06 | Código mantenible y ampliable por etapas. | Media |
| RNF-07 | Pruebas básicas de las clases principales. | Media |

## 3. Historias de usuario
Formato: *Como [rol], quiero [acción] para [beneficio].*

| ID | Historia | Criterios de aceptación | Prioridad |
|----|----------|-------------------------|-----------|
| HU-01 | Como **[PENDIENTE: rol]**, quiero registrar **[PENDIENTE: entidad]** para **[PENDIENTE: beneficio]**. | Los datos válidos se guardan; los inválidos muestran un mensaje claro en español. | Alta |
| HU-02 | Como **[PENDIENTE: rol]**, quiero consultar **[PENDIENTE: entidad]**. | Se muestran los datos guardados. | Alta |
| HU-03 | Como **[PENDIENTE: rol]**, quiero modificar **[PENDIENTE: entidad]**. | Los cambios quedan guardados y consultables. | Media |
| HU-04 | Como **[PENDIENTE: rol]**, quiero eliminar **[PENDIENTE: entidad]**. | El registro deja de aparecer; se pide confirmación. | Media |

## 4. Prioridades
- **Alta:** análisis, UML validado, dominio, persistencia, CRUD base, seguridad básica.
- **Media:** pruebas, mejoras de validación, documentación final.
- **Baja:** **[PENDIENTE]**
