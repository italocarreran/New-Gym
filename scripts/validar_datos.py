"""Valida los datos de ejercicios de la app.

Uso:  python scripts/validar_datos.py

Revisa que:
- cada músculo exista en data/musculos.json,
- cada fedb_id exista en free-exercise-db y cada og_id en openGym,
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
URL_IMG = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"


def cargar(nombre):
    return json.loads((DATA / nombre).read_text(encoding="utf-8"))


def main():
    musculos = cargar("musculos.json")
    catalogo = {e["id"]: e for e in cargar("ejercicios.json")["ejercicios"]}
    fedb = {e["id"]: e for e in cargar("fuentes/free-exercise-db.json")}
    ruta_og = DATA / "fuentes" / "opengym" / "biblioteca.json"
    og = {e["og_id"]: e for e in json.loads(ruta_og.read_text(encoding="utf-8"))["ejercicios"]} if ruta_og.exists() else {}
    grupos = musculos["grupos"]
    errores = []

    for e in catalogo.values():
        for m in [e["principal"], *e["secundarios"]]:
            if m not in grupos:
                errores.append(f"{e['id']}: músculo desconocido '{m}'")
        if e["fedb_id"] and e["fedb_id"] not in fedb:
            errores.append(f"{e['id']}: fedb_id '{e['fedb_id']}' no existe")
        if og and e.get("og_id") and e["og_id"] not in og:
            errores.append(f"{e['id']}: og_id '{e['og_id']}' no existe en openGym")

    if errores:
        print("ERRORES:")
        for err in errores:
            print("  -", err)
    else:
        print(f"OK: {len(catalogo)} ejercicios, todos los enlaces son válidos.")
    if og:
        con_es = sum(1 for e in catalogo.values() if og.get(e.get("og_id"), {}).get("instrucciones_idioma") == "es")
        print(f"Biblioteca openGym: {len(og)} ejercicios; {con_es} de los {len(catalogo)} del catálogo tienen instrucciones en español.")

    print("\nEjemplo de imagen:", URL_IMG + fedb[catalogo["pec_deck"]["fedb_id"]]["images"][0])
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
