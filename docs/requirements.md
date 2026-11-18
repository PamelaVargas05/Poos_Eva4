# Requerimientos

> Alcance inicial de referencia para EcoTech Solutions, basado en el material compartido del taller Clase 8. El caso detallado y el UML original deben confirmarse; atributos y reglas no indicados expresamente siguen pendientes.

## 1. Requerimientos funcionales
| ID | Descripción | Prioridad | Estado |
|----|-------------|-----------|--------|
| RF-01 | Representar departamentos, empleados, proyectos y registros de trabajo en el prototipo. | Alta | Propuesta del taller; validar con UML |
| RF-02 | Permitir que cada empleado se asocie a un departamento. | Alta | Relación de referencia |
| RF-03 | Relacionar cada registro de trabajo con un empleado y un proyecto. | Alta | Relación de referencia |
| RF-04 | Insertar inicialmente Department, Project y WorkRecord; insertar Employee como apoyo. | Alta | Implementación inicial |
| RF-05 | Persistir los datos del prototipo mediante SQLite y consultas parametrizadas. | Alta | Implementación inicial |
| RF-06 | Validar datos básicos y mostrar resultados/errores al usuario en español. | Alta | Implementación inicial |
| RF-07 | **[PENDIENTE]** Otros requerimientos del caso de negocio. | - | - |

Los requerimientos y relaciones anteriores se basan en el material compartido; el equipo debe confirmarlos antes de ampliar el alcance.

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
| HU-01 | Como integrante del equipo, quiero insertar un departamento y un proyecto para preparar los datos del prototipo. | Los DAO reciben identificadores generados por SQLite. | Alta |
| HU-02 | Como integrante del equipo, quiero registrar un empleado asociado a un departamento. | La FK del departamento se valida en SQLite. | Alta |
| HU-03 | Como integrante del equipo, quiero registrar horas de un empleado en un proyecto. | El registro conserva las dos FK, fecha y horas positivas. | Alta |

## 4. Prioridades
- **Alta:** análisis, UML validado, dominio, persistencia inicial, inserciones y seguridad básica.
- **Media:** pruebas, mejoras de validación, documentación final.
- **Baja:** **[PENDIENTE]**

## 5. Datos de referencia pendientes

Confirmar con el caso de negocio y el UML original los atributos de `Employee`, `Department`, `Project` y `WorkRecord`; tipos, restricciones, campos personales, unidades de horas y cualquier requerimiento adicional al flujo de inserción inicial.
