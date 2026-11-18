# Pruebas

Las pruebas usan `unittest` y una base SQLite en memoria para no crear datos de prueba permanentes.

Desde la raíz del repositorio, ejecutar:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas verifican atributos de lectura, cambios validados, asociaciones permitidas y rechazadas, vistas inmutables de las colecciones, creación de las cuatro tablas, inserciones relacionadas y rechazo de referencias inexistentes mediante claves foráneas.
