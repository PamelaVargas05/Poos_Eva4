# Requerimientos

> Alcance inicial de referencia para EcoTech Solutions, basado en el material compartido del taller Clase 8. El caso detallado y el UML original deben confirmarse; atributos y reglas no indicados expresamente siguen pendientes.

## 1. Requerimientos funcionales
| ID | Descripci├│n | Prioridad | Estado |
|----|-------------|-----------|--------|
| RF-01 | Representar departamentos, empleados, proyectos y registros de trabajo en el prototipo. | Alta | Propuesta del taller; validar con UML |
| RF-02 | Permitir que cada empleado se asocie a un departamento. | Alta | Relaci├│n de referencia |
| RF-03 | Relacionar cada registro de trabajo con un empleado y un proyecto. | Alta | Relaci├│n de referencia |
| RF-04 | Insertar inicialmente Department, Project y WorkRecord; insertar Employee como apoyo. | Alta | Implementaci├│n inicial |
| RF-05 | Persistir los datos del prototipo mediante SQLite y consultas parametrizadas. | Alta | Implementaci├│n inicial |
| RF-06 | Validar datos b├ísicos y mostrar resultados/errores al usuario en espa├▒ol. | Alta | Implementaci├│n inicial |
| RF-07 | **[PENDIENTE]** Otros requerimientos del caso de negocio. | - | - |

Los requerimientos y relaciones anteriores se basan en el material compartido; el equipo debe confirmarlos antes de ampliar el alcance.

## 2. Requerimientos no funcionales
| ID | Descripci├│n | Prioridad |
|----|-------------|-----------|
| RNF-01 | C├│digo, tablas y columnas en ingl├®s; documentaci├│n y mensajes al usuario en espa├▒ol. | Alta |
| RNF-02 | Encapsulamiento de atributos y separaci├│n de responsabilidades. | Alta |
| RNF-03 | Manejo de excepciones controlado, sin exponer detalles internos al usuario. | Alta |
| RNF-04 | Seguridad: sin credenciales en el repositorio; validaci├│n de entradas; consultas SQL parametrizadas. | Alta |
| RNF-05 | Coherencia entre el UML validado y el c├│digo. | Alta |
| RNF-06 | C├│digo mantenible y ampliable por etapas. | Media |
| RNF-07 | Pruebas b├ísicas de las clases principales. | Media |

## 3. Historias de usuario
Formato: *Como [rol], quiero [acci├│n] para [beneficio].*

| ID | Historia | Criterios de aceptaci├│n | Prioridad |
|----|----------|-------------------------|-----------|
| HU-01 | Como integrante del equipo, quiero insertar un departamento y un proyecto para preparar los datos del prototipo. | Los DAO reciben identificadores generados por SQLite. | Alta |
| HU-02 | Como integrante del equipo, quiero registrar un empleado asociado a un departamento. | La FK del departamento se valida en SQLite. | Alta |
| HU-03 | Como integrante del equipo, quiero registrar horas de un empleado en un proyecto. | El registro conserva las dos FK, fecha y horas positivas. | Alta |

## 4. Prioridades
- **Alta:** an├ílisis, UML validado, dominio, persistencia inicial, inserciones y seguridad b├ísica.
- **Media:** pruebas, mejoras de validaci├│n, documentaci├│n final.
- **Baja:** **[PENDIENTE]**

## 5. Datos de referencia pendientes

Confirmar con el caso de negocio y el UML original los atributos de `Employee`, `Department`, `Project` y `WorkRecord`; tipos, restricciones, campos personales, unidades de horas y cualquier requerimiento adicional al flujo de inserci├│n inicial.
