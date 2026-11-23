# Fuentes de datos y respaldo científico

Revisado el 23-11-2026.

## Recomendación

Usar **free-exercise-db** como base técnica (nombres, imágenes, instrucciones largas) y un **catálogo curado propio en español** (`data/ejercicios.json`) con el mapa de músculos, la fatiga y las alternativas. Ninguna base abierta trae lo que la app necesita para decidir alternativas: músculos con el detalle de la meta semanal (hombro lateral vs. posterior), peso de cada músculo, fatiga y explicaciones de equivalencia. Eso hay que curarlo, y ya está hecho para los 57 ejercicios de la rutina.

## Bases de ejercicios evaluadas

| Fuente | Licencia | Qué trae | Español | Veredicto |
|---|---|---|---|---|
| [free-exercise-db](https://github.com/yuhonas/free-exercise-db) | Unlicense (dominio público), datos e imágenes | 876 ejercicios en un JSON, 2 fotos por ejercicio, instrucciones en inglés, músculo principal/secundario, equipo, compuesto/aislado, nivel | No | **Usar.** Sin API, sin claves, sin restricciones. Copia en `data/fuentes/`. |
| [wger](https://github.com/wger-project/wger) | Código AGPL-3.0; datos de ejercicios con licencias Creative Commons por entrada (en general CC-BY-SA) | API abierta, traducciones a varios idiomas incluido español, imágenes y videos subidos por la comunidad | Parcial | **Complemento opcional** para traducir instrucciones. Exige atribución por ejercicio y la cobertura en español es desigual. Su API no fue accesible desde este entorno, así que no la descargué. |
| ExerciseDB (RapidAPI / exercisedb.dev) | Términos propios del proveedor, no es licencia abierta | 1.300+ ejercicios con GIFs animados | No | **No usar** como base. Los GIFs son de un proveedor comercial y no pude leer los términos (página en Notion que requiere navegador). Para una app personal no vale el riesgo ni la dependencia de una API con cuota. |
| ExRx, MuscleWiki | Licencias comerciales / términos de API restrictivos | Muy buen contenido técnico | No | Solo como referencia de lectura, no para copiar datos. |

### Límites de free-exercise-db que el catálogo curado corrige
- Agrupa todo el hombro en `shoulders`: no distingue lateral, posterior ni anterior, que son metas separadas en la app.
- Los secundarios son ruidosos (por ejemplo, el peso muerto rumano lista pantorrillas). Para ponderar series se usan solo los secundarios que realmente cuentan.
- No tiene pec deck con ese nombre (`Butterfly`), ni elevación lateral en máquina (queda sin imagen).
- Algunas imágenes no coinciden exacto: la búlgara apunta a la zancada estática con mancuernas, y la prensa con pies bajos reutiliza la prensa normal. Está anotado en la técnica de cada uno.

Las imágenes se pueden cargar directo desde
`https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/<ruta de images>`
o copiarse al repo más adelante si se quiere que la app funcione sin internet.

## Respaldo para las reglas de intensidad (RIR / fallo)

- **Refalo, Helms, Trexler, Hamilton y Fyfe (2023), Sports Medicine.** Meta-análisis de 15 estudios: entrenar al fallo da, como mucho, una ventaja trivial en hipertrofia frente a quedarse cerca del fallo (ES 0,19; y sin diferencia en el subgrupo de fallo momentáneo). [Registro](https://dro.deakin.edu.au/articles/journal_contribution/Influence_of_Resistance_Training_Proximity-to-Failure_on_Skeletal_Muscle_Hypertrophy_A_Systematic_Review_with_Meta-analysis/22030796)
- **Robinson, Pelland, Remmert, Refalo, Jukic, Steele y Zourdos (2024), Sports Medicine.** Meta-regresiones con RIR estimado: la hipertrofia aumenta a medida que las series se acercan al fallo, mientras que la fuerza mejora parecido en un rango amplio de RIR. [Preprint](https://sportrxiv.org/index.php/server/preprint/view/295)

**Cómo se traduce a la app:** compuestos a 1-2 RIR (casi todo el beneficio, menos fatiga para las series siguientes y menos riesgo con cargas pesadas); aislados con la última serie al fallo o a 1 RIR (fatiga local barata, bajo riesgo). Coincide con las reglas del proyecto. La evidencia respalda "cerca del fallo" en general; la división exacta compuesto/aislado es una aplicación práctica habitual, no un resultado directo de estos estudios.

## Respaldo para el volumen semanal por músculo

- **Pelland, Remmert, Robinson, Hinson y Zourdos (2024), preprint en SportRxiv.** Meta-regresión de 67 estudios y 2.058 participantes: más series semanales dan más hipertrofia y fuerza, con rendimientos decrecientes. El método que mejor explicó los datos fue el **"fraccional"**: las series indirectas cuentan 0,5. [Preprint](https://sportrxiv.org/index.php/server/preprint/view/460)

**Cómo se traduce a la app:** el conteo principal = 1 y secundario = 0,5 es exactamente el método fraccional de ese análisis. Las metas de 8-16 series duras por músculo están dentro del rango que los estudios cubren con buenos resultados. No hay un número "mágico": más volumen ayuda pero cada serie extra rinde menos, por eso las metas son rangos.

## Hallazgo al cruzar la rutina con las metas

`python scripts/validar_datos.py` suma las series de los días 1-3 (alternativa A, ponderadas). La rutina base deja cortas todas las metas:

| Músculo | Días 1-3 | Meta |
|---|---|---|
| Espalda | 11 | 14-16 |
| Pecho | 8 | 12-14 |
| Cuádriceps | 7 | 10-12 |
| Isquios y glúteos | 8,5 | 10-12 |
| Hombro lateral | 4 | 8-10 |
| Hombro posterior | 6 | 8-10 |
| Tríceps | 7 | 8-10 |
| Bíceps | 7,5 | 8-10 |
| Pantorrillas | 3 | 6-8 |

El faltante total (~26 series) es mayor que lo que cabe en un día 4 de rescate de 60-70 minutos. Hay que decidir entre subir series en los días 1-3, hacer que el día 4 sea fijo de tren superior más pantorrillas, o bajar las metas al nivel de la rutina.
