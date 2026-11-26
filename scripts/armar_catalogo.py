#!/usr/bin/env python3
"""Arma app/catalogo.js a partir de data/ (ejercicios, músculos y textos de openGym).

    python3 scripts/armar_catalogo.py

La app publicada solo ve la carpeta app/, así que el catálogo se copia ahí.
Correrlo cada vez que cambie data/ejercicios.json o data/musculos.json.
verificar.sh avisa si quedó desactualizado.
"""
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "app" / "catalogo.js"

# claves cortas que usa la interfaz (las mismas del prototipo y del muñeco)
CORTO = {
    "espalda": "espalda", "pecho": "pecho", "cuadriceps": "cuad", "isquios_gluteos": "isq",
    "hombro_lateral": "lat", "hombro_posterior": "post", "triceps": "tri", "biceps": "bi",
    "pantorrillas": "pant", "hombro_anterior": "front", "abdomen": "abs", "lumbar": "lumbar",
    "antebrazo": "ante",
}
EQUIPO = {
    "barra": "Barra", "mancuernas": "Mancuernas", "maquina": "Máquina", "polea": "Polea",
    "peso_corporal": "Sin máquina", "smith": "Smith", "otro": "Otro",
}
PATRON = {
    "empuje_horizontal": "empuje horizontal", "empuje_inclinado": "empuje inclinado",
    "empuje_vertical": "empuje vertical", "empuje_vertical_abajo": "empuje hacia abajo",
    "tiron_horizontal": "tirón horizontal", "tiron_vertical": "tirón vertical",
    "bisagra_cadera": "bisagra de cadera", "dominante_rodilla": "dominante de rodilla",
    "unilateral_pierna": "pierna a una pierna", "extension_rodilla": "extensión de rodilla",
    "flexion_rodilla": "flexión de rodilla", "flexion_plantar": "pantorrilla",
    "aduccion_horizontal": "cerrar los brazos", "abduccion_hombro": "elevación lateral",
    "abduccion_horizontal": "abrir los brazos atrás", "extension_hombro": "extensión de hombro",
    "flexion_codo": "flexión de codo", "extension_codo": "extensión de codo",
    "flexion_tronco": "flexión de tronco", "anti_extension": "estabilidad del tronco",
}
FOTOS = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"


def main():
    ej = json.loads((RAIZ / "data/ejercicios.json").read_text(encoding="utf-8"))["ejercicios"]
    mus = json.loads((RAIZ / "data/musculos.json").read_text(encoding="utf-8"))
    og = {e["og_id"]: e for e in json.loads(
        (RAIZ / "data/fuentes/opengym/biblioteca.json").read_text(encoding="utf-8"))["ejercicios"]}
    fedb = {e["id"]: e for e in json.loads(
        (RAIZ / "data/fuentes/free-exercise-db.json").read_text(encoding="utf-8"))}

    MUS = {CORTO[k]: g["nombre"] for k, g in mus["grupos"].items()}
    EX = {}
    for e in ej:
        pat = PATRON.get(e["patron"], e["patron"].replace("_", " "))
        o = og.get(e.get("og_id") or "")
        f = fedb.get(e.get("fedb_id") or "")
        como = (o or {}).get("instrucciones") or [e["tecnica"]]
        EX[e["id"]] = {
            "n": e["nombre"],
            "eq": EQUIPO.get(e["equipo"], e["equipo"]),
            "p": [CORTO[e["principal"]]],
            "s": [CORTO[m] for m in e["secundarios"]],
            "comp": e["mecanica"] == "compuesto",
            "fat": e["fatiga"],
            "pat": e["patron"],
            "why": f"Patrón {pat}; principal {MUS[CORTO[e['principal']]].lower()}.",
            "adj": "Si es la primera vez, parte liviano y busca el mínimo del rango con 1-2 en reserva.",
            "tec": e["tecnica"],
            "como": como,
            "img": [FOTOS + i for i in (f or {}).get("images", [])[:2]],
        }
    salida = (
        "// Generado por scripts/armar_catalogo.py desde data/. No editar a mano.\n"
        "window.CATALOGO = " + json.dumps({"MUS": MUS, "EX": EX}, ensure_ascii=False, indent=0) + ";\n"
    )
    if "--revisar" in sys.argv:
        if not SALIDA.exists() or SALIDA.read_text(encoding="utf-8") != salida:
            print("app/catalogo.js está desactualizado: corre python3 scripts/armar_catalogo.py")
            sys.exit(1)
        return
    SALIDA.write_text(salida, encoding="utf-8")
    print(f"app/catalogo.js: {len(EX)} ejercicios")


if __name__ == "__main__":
    main()
