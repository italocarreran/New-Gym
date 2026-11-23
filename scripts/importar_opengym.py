"""Importa el catálogo de texto de openGym a una biblioteca compacta en español.

Uso:
    git clone --depth 1 https://github.com/DuarteSantos8/openGym /tmp/opengym
    python scripts/importar_opengym.py /tmp/opengym

Genera data/fuentes/opengym/biblioteca.json con un ejercicio por entrada:
nombre en español e inglés, equipo, tipo de máquina, músculos de openGym y
traducidos a los grupos de la app, e instrucciones (español si existen).

NO copia imágenes ni animaciones: en openGym están licenciadas por Gym visual
solo para esa app (ver catalogue/media/NOTICE.md del repo original).
Las variantes "versión femenina" (variantOf) se omiten porque repiten el texto.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "data" / "fuentes" / "opengym" / "biblioteca.json"

# Músculos de openGym -> grupos de data/musculos.json (None = no se cuenta)
MUSCULO = {
    "pectorals": "pecho", "chest": "pecho", "upper chest": "pecho",
    "lats": "espalda", "latissimus dorsi": "espalda", "upper back": "espalda",
    "back": "espalda", "rhomboids": "espalda", "traps": "espalda", "trapezius": "espalda",
    "quads": "cuadriceps", "quadriceps": "cuadriceps",
    "glutes": "isquios_gluteos", "hamstrings": "isquios_gluteos",
    "side delts": "hombro_lateral", "rear delts": "hombro_posterior", "front delts": "hombro_anterior",
    "triceps": "triceps", "biceps": "biceps", "brachialis": "biceps",
    "calves": "pantorrillas", "soleus": "pantorrillas",
    "abs": "abdomen", "abdominals": "abdomen", "lower abs": "abdomen", "obliques": "abdomen", "core": "abdomen",
    "spine": "lumbar", "lower back": "lumbar",
    "forearms": "antebrazo", "grip muscles": "antebrazo", "wrist flexors": "antebrazo", "wrist extensors": "antebrazo",
}

EQUIPO = {
    "barbell": "barra", "olympic barbell": "barra", "ez barbell": "barra", "trap bar": "barra",
    "dumbbell": "mancuernas", "cable": "polea", "rope": "polea",
    "leverage machine": "maquina", "sled machine": "maquina", "assisted": "maquina",
    "smith machine": "smith", "body weight": "peso_corporal", "weighted": "peso_corporal",
    "kettlebell": "kettlebell", "band": "banda", "resistance band": "banda",
}


def main(ruta_clon):
    cat = Path(ruta_clon) / "catalogue"
    es = json.loads((cat / "i18n" / "es.json").read_text(encoding="utf-8"))
    salida = []
    for f in sorted((cat / "exercises").glob("*.json")):
        e = json.loads(f.read_text(encoding="utf-8"))
        if "name" not in e or e.get("variantOf"):
            continue
        t = es.get(e["id"], {})
        principal = MUSCULO.get(e.get("target"))
        secundarios = []
        for m in e.get("secondaryMuscles", []):
            g = MUSCULO.get(m)
            if g and g != principal and g not in secundarios:
                secundarios.append(g)
        salida.append({
            "og_id": e["id"],
            "nombre": t.get("name") or e["name"],
            "nombre_en": e["name"],
            "categoria": e.get("category"),
            "equipo": EQUIPO.get(e.get("equipment"), "otro"),
            "equipo_og": e.get("equipment"),
            "maquina": e.get("machineKind"),
            "necesita": e.get("needs", []),
            "principal": principal,
            "secundarios": secundarios,
            "musculo_og": e.get("target"),
            "secundarios_og": e.get("secondaryMuscles", []),
            "descripcion_en": e.get("description"),
            "instrucciones": t.get("instructions") or e.get("instructions", []),
            "instrucciones_idioma": "es" if t.get("instructions") else "en",
            "fuente_texto": e.get("textSource"),
        })
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps({"ejercicios": salida}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    con_es = sum(1 for x in salida if x["instrucciones_idioma"] == "es")
    print(f"{len(salida)} ejercicios -> {SALIDA.relative_to(RAIZ)} ({con_es} con instrucciones en español)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
