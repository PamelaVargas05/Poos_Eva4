# Arquitectura

## 1. Estado actual (requisitos de Clase 1 y Clase 2)

- `src/domain/`: entidades con atributos privados, propiedades de lectura, validaci├│n de cambios y asociaciones controladas.
- `src/persistence/`: conexi├│n SQLite, creaci├│n de tablas y DAO de inserci├│n.
- `src/main.py`: punto de entrada de la demostraci├│n y creaci├│n de relaciones entre los objetos.
- `tests/`: pruebas del dominio, asociaciones permitidas/rechazadas, esquema, inserciones y claves for├íneas.

El modelo es una referencia del material del taller, no el UML original validado.

## 2. Responsabilidad del dominio
La capa `domain` contiene las clases que representan el negocio, con sus atributos encapsulados, sus reglas y sus relaciones tal como est├®n en el UML validado. Debe ser independiente de la base de datos y de la interfaz con el usuario.

## 3. Alcance y ampliaci├│n

Se mantiene la implementaci├│n sencilla. No se agregan `Service`, `Controller`, DAO gen├®rico ni patrones adicionales.

| Etapa | Componente posible | Cu├índo |
|-------|--------------------|--------|
| Ampliar el dominio | Entidades y reglas confirmadas por UML | Despu├®s de validar el modelo. |
| Ampliar persistencia | Operaciones DAO adicionales si se requieren | Cuando el alcance funcional las solicite. |
| Interfaz | Men├║ de consola u otra **[PENDIENTE]** | Cuando se defina. |
| Configuraci├│n | Variables de entorno si se incorporan credenciales | Solo si un servicio futuro lo necesita. |

Principio gu├¡a: separaci├│n de responsabilidades; el dominio no ejecuta SQL y la persistencia centraliza las consultas parametrizadas.
