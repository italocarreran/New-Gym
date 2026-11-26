# MAPA.md · dónde está cada cosa

Léelo antes de abrir archivos. Abre completo **solo** el archivo que vas a modificar.

## Estructura

```
REGLAS.md              obligatorio: leer primero, siempre
DECISIONES.md          lo vigente (producto, stack, progresión, UI)
BITACORA.md            en curso, pendientes abiertos y registro de sesiones
AGENTS.md              cómo se trabaja acá (CLAUDE.md apunta a este)
MAPA.md                este archivo
ROADMAP.md             plan por etapas
README.md              presentación para humanos
prototipo/
  index.html           prototipo interactivo, un solo archivo (HTML+CSS+JS)
app/                   la PWA que se publica (GitHub Pages, ver docs/instalar-en-el-celular.md)
  index.html           pantallas (vienen del prototipo) + "Registro real" (guardar/leer con datos/) + "Cuenta" (login)
  catalogo.js          GENERADO por scripts/armar_catalogo.py desde data/; no editar a mano
  sw.js                service worker (sin señal); manifest.webmanifest e iconos/ para instalar
  config.ejemplo.js    molde de config.js (URL + clave pública de Supabase); config.js no va al repo
  datos/               capa de datos: lo único que lee y guarda (ver datos/LEEME.md)
    index.js           API crearDatos() y sincronización
    local.js           copia local en IndexedDB, una base por usuario
    remoto.js          cliente mínimo de Supabase por HTTP
    prueba.html        página para probar cuenta, series y sincronización
supabase/
  esquema.sql          tablas rutinas/sesiones/series/ajustes, triggers y permisos (RLS)
  LEEME.md             cómo crear el proyecto Supabase y publicar
data/
  ejercicios.json      catálogo curado: 57 ejercicios, músculos, fedb_id, og_id, equivalencias
  musculos.json        grupos musculares, pesos del conteo, metas (null = las pone el usuario)
  fuentes/             datos de terceros, no se editan a mano
    free-exercise-db.json        copia completa (dominio público)
    opengym/biblioteca.json      solo texto de openGym (AGPL/MIT) + licencias
    LEEME.md                     de dónde salen y cómo actualizarlos
  iconos/
    lista-150-ejercicios.csv     150 ejercicios para dibujar íconos (UTF-8 con BOM)
docs/
  contexto-app-entrenamiento.md  requisitos originales (2026-11-23)
  fuentes-de-datos.md            evaluación de bases de ejercicios y respaldo científico
  img/                           capturas: mapa de calor, encabezado, muestra de íconos
scripts/
  sincronizar.sh       trae main al día y muestra qué llegó
  verificar.sh         datos + sintaxis del prototipo y de app/ + secretos → "TODO OK"
  validar_datos.py     coherencia de data/
  armar_catalogo.py    data/ → app/catalogo.js (verificar.sh avisa si quedó viejo)
  importar_opengym.py  regenera data/fuentes/opengym/biblioteca.json
herramientas/iconos/   prototipo del generador de íconos (MediaPipe → SVG)
```

## `prototipo/index.html` por dentro

Un solo `<script>`. Usa **datos de ejemplo propios**, no lee `data/`.

| Nombre | Qué es |
|---|---|
| `MUS`, `META`, `BASE` | grupos musculares, metas de ejemplo y lo hecho en la semana (ejemplo) |
| `EX` | ejercicios de ejemplo: `n` nombre, `eq` equipo, `p`/`s` músculos, `why` equivalencia, `adj` ajuste de peso, `last` sesión anterior |
| `TEC` | técnica por ejercicio (`como`, `ojo`) |
| `RUT` | rutinas guardadas en orden de rotación (`name`, `last`, `slots`); `nextRut()` dice cuál toca, `rutMins()` estima minutos |
| `DAY` | slots de la rutina que se mira (`let`; `useDay(k)` lo apunta a `RUT[k].slots`): series, rango de reps, prioridad, `comp`/`iso`, alternativas A/B/C |
| `IMG` | fotos de free-exercise-db **en base64, una línea de ~270 KB**. No la leas: búscala o sáltatela |
| `S` | estado global de la app |
| `act(a, v)` | único despachador de acciones (los botones llevan `data-a` / `data-v`) |
| `plan`, `target`, `feedback`, `progressionNote` | progresión y meta de hoy |
| `weekly` | conteo semanal ponderado |
| `timePlan`, `cutSet` | qué recortar si falta tiempo |
| `findFiller`, `conflictFor`, `reorderCheck` | relleno mientras se espera y avisos de orden |
| `bodyFigure`, `bodySvg`, `REGION_GRUPO`, `FRONT`, `BACK` | muñeco del mapa de calor (SVG a mano) |
| `bodyFab` | muñeco + conteo en el encabezado |
| `HOY`, `HIST`, `viewInicioApp` | pestaña Inicio: puntaje de cumplimiento (`CUMP`: músculos 55 + días 25 + esfuerzo 20; `cumpSemana`, `musSemana`, `ptsSesion`) y calendario de días entrenados (historial de ejemplo) |
| `viewInicio` | inicio de Rutina: la que toca, las demás y "+ Crear rutina" (`S.home`, `S.rut`, `S.edRut`, `S.lastDone`) |
| `viewHoy`, `slotCard`, `viewSemana`, `viewGuia`, `pickerHtml` | vistas |

Pestañas (clave interna → nombre en pantalla): `inicio` → Inicio, `hoy` → Sesión, (`semana` ya no está en la barra; `viewSemana` queda sin uso), `rutina` → Editar, `guia` → Esfuerzo.

## `data/ejercicios.json`

Objeto con `_nota` y `ejercicios`. Cada ejercicio trae sus músculos con los grupos de `musculos.json`, el `fedb_id` (foto en free-exercise-db) y el `og_id` (texto en openGym). Las fotos se cargan desde `https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/<ruta>`.
