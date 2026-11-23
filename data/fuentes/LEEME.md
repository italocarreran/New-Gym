# Datos de terceros

`free-exercise-db.json`: copia de https://github.com/yuhonas/free-exercise-db (`dist/exercises.json`, descargado el 23-11-2026).
Licencia: Unlicense (dominio público). Las imágenes se cargan desde
`https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/<images[i]>`.

Para actualizar:

    curl -L -o data/fuentes/free-exercise-db.json https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json
    python scripts/validar_datos.py
