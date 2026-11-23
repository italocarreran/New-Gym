"""Valida los datos de la app y muestra el volumen semanal que da la rutina base.

Uso:  python scripts/validar_datos.py

Revisa que:
- cada ejercicio de la rutina exista en el catálogo,
- cada músculo exista en data/musculos.json,
- cada fedb_id exista en free-exercise-db y cada og_id en openGym,
- cada slot tenga 3 alternativas con el mismo músculo principal.
Luego suma las series ponderadas de los días 1-3 usando la alternativa A
y las compara con la meta semanal.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
URL_IMG = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"


def cargar(nombre):
    return json.loads((DATA / nombre).read_text(encoding="utf-8"))


def main():
    musculos = cargar("musculos.json")
    catalogo = {e["id"]: e for e in cargar("ejercicios.json")["ejercicios"]}
    rutina = cargar("rutina.json")
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

    volumen = defaultdict(float)
    w_p, w_s = musculos["pesos"]["principal"], musculos["pesos"]["secundario"]
    for dia in rutina["dias"]:
        for slot in dia.get("slots", []):
            alts = slot["alternativas"]
            if len(alts) != 3:
                errores.append(f"{slot['id']}: tiene {len(alts)} alternativas (deben ser 3)")
            ids = [a["ejercicio"] for a in alts]
            faltan = [i for i in ids if i not in catalogo]
            if faltan:
                errores.append(f"{slot['id']}: ejercicios no catalogados {faltan}")
                continue
            principales = {catalogo[i]["principal"] for i in ids}
            if len(principales) > 1:
                errores.append(f"{slot['id']}: alternativas con distinto músculo principal {principales}")
            a = catalogo[ids[0]]
            volumen[a["principal"]] += slot["series"] * w_p
            for m in a["secundarios"]:
                volumen[m] += slot["series"] * w_s

    if errores:
        print("ERRORES:")
        for err in errores:
            print("  -", err)
    else:
        print(f"OK: {len(catalogo)} ejercicios, todos los enlaces son válidos.")
    if og:
        con_es = sum(1 for e in catalogo.values() if og.get(e.get("og_id"), {}).get("instrucciones_idioma") == "es")
        print(f"Biblioteca openGym: {len(og)} ejercicios; {con_es} de los {len(catalogo)} del catálogo tienen instrucciones en español.")

    print("\nVolumen semanal de la rutina base (días 1-3, alternativa A, ponderado):")
    for clave, g in grupos.items():
        meta = g["meta_semanal"]
        v = volumen.get(clave, 0)
        if meta:
            estado = "ok" if v >= meta[0] else f"falta {meta[0] - v:g}"
            print(f"  {g['nombre']:<18} {v:>5g}  meta {meta[0]}-{meta[1]}  {estado}")
        elif v:
            print(f"  {g['nombre']:<18} {v:>5g}  (sin meta)")

    print("\nEjemplo de imagen:", URL_IMG + fedb[catalogo["pec_deck"]["fedb_id"]]["images"][0])
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
