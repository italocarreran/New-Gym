# Datos de terceros

`free-exercise-db.json`: copia de https://github.com/yuhonas/free-exercise-db (`dist/exercises.json`, descargado el 23-11-2026).
Licencia: Unlicense (dominio público). Las imágenes se cargan desde
`https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/<images[i]>`.

Para actualizar:

    curl -L -o data/fuentes/free-exercise-db.json https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json
    python scripts/validar_datos.py

`opengym/biblioteca.json`: texto del catálogo de https://github.com/DuarteSantos8/openGym (commit e4a68a9, 15-11-2026),
generado con `python scripts/importar_opengym.py <clon>`. Licencia del texto: AGPL-3.0 (lo escrito por openGym) y MIT
(entradas `fuente_texto: exercisedb`, © 2026 Hasan Emir Yıldırım, vía ExerciseDB v1 de AscendAPI). Copia de la AGPL en `opengym/`.
Las imágenes y animaciones de openGym NO se incluyen: están licenciadas por Gym visual solo para openGym.
