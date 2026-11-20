# Revisión histórica del modelo EcoTech

> Esta revisión corresponde al prototipo EcoTech/SQLite y no valida el UML de Viajes Aventura. Para el modelo turístico, consultar `docs/uml.md`; la revisión académica sigue pendiente.

## Alcance revisado

Se revisó el texto de instrucciones compartido para el taller y se registró una propuesta de cuatro entidades: `Department`, `Employee`, `Project` y `WorkRecord`. El repositorio no contiene el UML original de la evaluación anterior. `docs/UML_base_v1.md` conserva la referencia de trabajo EcoTech; `docs/uml.md` ahora corresponde a Viajes Aventura y no forma parte de esta revisión histórica.

## Observaciones

- Las relaciones `Department 1 — 0..* Employee`, `Employee 1 — 0..* WorkRecord` y `Project 1 — 0..* WorkRecord` fueron proporcionadas en el material del taller.
- `WorkRecord` actúa como enlace entre un empleado y un proyecto.
- Los campos `name`, `work_date` y `hours`, sus tipos, y los nombres de las claves son supuestos mínimos para probar el flujo de inserción; el material no especifica el conjunto completo de atributos del UML original.
- `Employee` se usa como entidad de apoyo para poder satisfacer las claves foráneas de `WorkRecord`.
- No se incorporaron herencia ni patrones adicionales.

## Confirmaciones requeridas

1. Comparar el modelo de referencia con el UML real de la evaluación anterior.
2. Confirmar nombres, responsabilidades, visibilidad, atributos, tipos, métodos y reglas de negocio.
3. Confirmar que cada empleado pertenece a un solo departamento y que ambos extremos de `WorkRecord` son obligatorios.
4. Confirmar la representación de fechas y horas y las restricciones para ellas.
5. Obtener acuerdo del equipo y, si corresponde, validación docente antes de considerar el modelo definitivo.

No se afirma que el UML haya sido validado por el equipo o por el docente.
