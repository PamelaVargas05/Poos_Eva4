# Poos_Eva4

## Descripción
Proyecto de la asignatura **Programación Orientada a Objetos Seguros**, desarrollado progresivamente en Python.

> **[PENDIENTE]** Agregar aquí la descripción definitiva del sistema cuando el caso de negocio esté confirmado.

## Objetivo
Construir una solución aplicando Programación Orientada a Objetos, coherencia entre UML y código, encapsulamiento, relaciones y herencia (cuando corresponda), integración con base de datos, operaciones CRUD, manejo de excepciones y buenas prácticas de seguridad, trabajando con Jira (Kanban) y GitHub.

## Tecnologías
- Python 3.10 o superior
- SQLite o MySQL **[PENDIENTE: definir]**
- Git y GitHub (control de versiones)
- Jira, tablero Kanban (gestión ágil)

## Estructura de carpetas
```
Poos_Eva4/
├── docs/                    Documentación del proyecto (en español)
│   ├── requirements.md
│   ├── uml.md
│   ├── architecture.md
│   ├── development_plan.md
│   └── decisions.md
├── src/                     Código fuente (en inglés)
│   ├── domain/              Clases del dominio
│   │   └── __init__.py
│   └── main.py              Punto de entrada
├── tests/                   Pruebas
│   └── README.md
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación
1. Instalar Python 3.10+ desde https://www.python.org/downloads/ (marcar **Add Python to PATH**).
2. Verificar: `python --version`
3. Crear el entorno virtual (en la raíz del proyecto):
   ```
   python -m venv .venv
   ```
4. Activarlo en Windows (PowerShell):
   ```
   .venv\Scripts\Activate.ps1
   ```
   Si PowerShell bloquea el script: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
   En CMD: `.venv\Scripts\activate.bat`
5. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución inicial
```
python src/main.py
```
Debe mostrar un mensaje de proyecto inicializado.

## Flujo de trabajo con GitHub
- No se trabaja directamente sobre `main`.
- Cada tarjeta de Jira se desarrolla en una rama propia, por ejemplo `feature/<short-name>`.
- Commits pequeños, con mensajes claros.
- Se abre un Pull Request y la otra integrante lo revisa antes de fusionarlo a `main`.
- Nunca se suben credenciales, archivos `.env` ni bases de datos (`*.db`).

## Integrantes
- Pamela
- Valentina
