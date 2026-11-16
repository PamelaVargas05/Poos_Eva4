# Arquitectura

## 1. Estado actual (etapa inicial)
El proyecto solo tiene lo necesario para comenzar:
- `src/domain/`: paquete donde irán las clases del negocio.
- `src/main.py`: punto de entrada.

No se han creado capas adicionales porque aún no existen requisitos que las justifiquen.

## 2. Responsabilidad del dominio
La capa `domain` contiene las clases que representan el negocio, con sus atributos encapsulados, sus reglas y sus relaciones tal como estén en el UML validado. Debe ser independiente de la base de datos y de la interfaz con el usuario.

## 3. Ampliación en etapas posteriores
Se agregarán componentes solo cuando una tarjeta de Jira los necesite:

| Etapa | Componente posible | Cuándo |
|-------|--------------------|--------|
| Persistencia | Paquete para acceso a datos (por ejemplo `src/repository/`) | Al integrar SQLite o MySQL |
| CRUD | Servicios o casos de uso (por ejemplo `src/services/`) | Al implementar operaciones CRUD |
| Interfaz | Menú de consola u otra **[PENDIENTE]** | Cuando se defina |
| Configuración | Lectura de variables de entorno (`.env.example` con valores ficticios) | Si se usa MySQL u otras credenciales |
| Excepciones | Excepciones propias del proyecto | Al manejar errores de negocio |

Principio guía: separación de responsabilidades; el dominio no depende de las capas externas.
