# Revisi├│n del modelo UML de referencia

## Alcance revisado

Se revis├│ el texto de instrucciones compartido para el taller y se registr├│ una propuesta de cuatro entidades: `Department`, `Employee`, `Project` y `WorkRecord`. El repositorio no contiene el UML original de la evaluaci├│n anterior. Por eso, `docs/uml.md` y `docs/UML_base_v1.md` describen una referencia de trabajo, no una copia validada.

## Observaciones

- Las relaciones `Department 1 ÔÇö 0..* Employee`, `Employee 1 ÔÇö 0..* WorkRecord` y `Project 1 ÔÇö 0..* WorkRecord` fueron proporcionadas en el material del taller.
- `WorkRecord` act├║a como enlace entre un empleado y un proyecto.
- Los campos `name`, `work_date` y `hours`, sus tipos, y los nombres de las claves son supuestos m├¡nimos para probar el flujo de inserci├│n; el material no especifica el conjunto completo de atributos del UML original.
- `Employee` se usa como entidad de apoyo para poder satisfacer las claves for├íneas de `WorkRecord`.
- No se incorporaron herencia ni patrones adicionales.

## Confirmaciones requeridas

1. Comparar el modelo de referencia con el UML real de la evaluaci├│n anterior.
2. Confirmar nombres, responsabilidades, visibilidad, atributos, tipos, m├®todos y reglas de negocio.
3. Confirmar que cada empleado pertenece a un solo departamento y que ambos extremos de `WorkRecord` son obligatorios.
4. Confirmar la representaci├│n de fechas y horas y las restricciones para ellas.
5. Obtener acuerdo del equipo y, si corresponde, validaci├│n docente antes de considerar el modelo definitivo.

No se afirma que el UML haya sido validado por el equipo o por el docente.
