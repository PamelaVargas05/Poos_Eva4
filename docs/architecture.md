# Arquitectura

## 1. Estado actual (requisitos de Clase 1 y Clase 2)

- `src/domain/`: entidades con atributos privados, propiedades de lectura, validación de cambios y asociaciones controladas.
- `src/persistence/`: conexión SQLite, creación de tablas y DAO de inserción.
- `src/main.py`: punto de entrada de la demostración y creación de relaciones entre los objetos.
- `tests/`: pruebas del dominio, asociaciones permitidas/rechazadas, esquema, inserciones y claves foráneas.

El modelo es una referencia del material del taller, no el UML original validado.

## 2. Responsabilidad del dominio
La capa `domain` contiene las clases que representan el negocio, con sus atributos encapsulados, sus reglas y sus relaciones tal como estén en el UML validado. Debe ser independiente de la base de datos y de la interfaz con el usuario.

## 3. Alcance y ampliación

Se mantiene la implementación sencilla. No se agregan `Service`, `Controller`, DAO genérico ni patrones adicionales.

| Etapa | Componente posible | Cuándo |
|-------|--------------------|--------|
| Ampliar el dominio | Entidades y reglas confirmadas por UML | Después de validar el modelo. |
| Ampliar persistencia | Operaciones DAO adicionales si se requieren | Cuando el alcance funcional las solicite. |
| Interfaz | Menú de consola u otra **[PENDIENTE]** | Cuando se defina. |
| Configuración | Variables de entorno si se incorporan credenciales | Solo si un servicio futuro lo necesita. |

Principio guía: separación de responsabilidades; el dominio no ejecuta SQL y la persistencia centraliza las consultas parametrizadas.
