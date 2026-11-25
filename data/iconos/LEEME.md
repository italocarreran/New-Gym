# Lista de 150 ejercicios para íconos

`lista-150-ejercicios.csv` reúne los 150 ejercicios de gimnasio más usados, para dibujar los íconos propios de la app (figura plana, músculos en rojo, dos cuadros inicio/fin).

- Incluye 56 del catálogo de la app (`data/ejercicios.json`, columna `en_catalogo_app = sí`; "Prensa con pies bajos" comparte foto con "Prensa de piernas" y no se repite) más 94 comunes que faltaban.
- `foto_inicio` / `foto_fin`: fotos de dominio público de free-exercise-db (yuhonas/free-exercise-db), solo como referencia de postura. Todos los enlaces se verificaron (HTTP 200) el 2026-11-24.
- `musculo_principal` / `musculos_secundarios`: vienen de free-exercise-db, traducidos. En hombro se indica la cabeza del deltoides según el grupo de la app.
- `grupo`: grupo muscular que usa la app para contar series.
- 3 ejercicios comunes no están en free-exercise-db (`en_free_exercise_db = NO`); la columna `nota` dice qué foto usar de referencia.
- No usar imágenes de openGym ni de ExerciseDB.
- Archivo en UTF-8 con BOM para que Excel muestre bien los acentos.
