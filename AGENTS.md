# AGENTS.md · cómo se trabaja en este repo

> Para cualquier IA (Claude, ChatGPT, Codex, Cursor) o persona que llegue. Documento vivo: si descubres algo que la próxima sesión necesita saber, agrégalo antes de cerrar.

## 0. Orden de lectura

1. **`REGLAS.md`**, entero. Obligatorio.
2. **`DECISIONES.md`**, entero. Lo vigente.
3. **`BITACORA.md`**: "En curso", "Pendientes abiertos" y las últimas entradas.
4. **`MAPA.md`**: dónde está cada cosa.
5. Abre completo **solo el archivo que vas a modificar**. No abras vecinos "para tener contexto".

## 1. Qué es

App personal de gimnasio en español. Resuelve: alternativa equivalente al toque cuando una máquina está ocupada (slots con A/B/C), series duras por músculo en la semana, y cuándo subir peso. Requisitos originales en `docs/contexto-app-entrenamiento.md`; lo vigente en `DECISIONES.md`.

**Estado (2026-11-26):** la PWA v1 está en `app/` (pantallas del prototipo + registro en Supabase) y se publica en GitHub Pages desde `main`. `prototipo/` queda como referencia de UI. Ver `ROADMAP.md`.

## 2. Cómo se entregan los cambios

- Rama propia desde `main` → `bash scripts/verificar.sh` en `TODO OK` → PR o merge a `main` → borrar la rama.
- Commits en español, cortos ("Agrega…", "Corrige…"). Si no eres Claude, prefijo con tu nombre (`codex:`, `chatgpt:`).
- Si eres un hilo de Claude en el proyecto "App GYM": tu rama de trabajo es la que te asignó la sesión; igual sale de `main` y vuelve a `main`.
- **Si eres Codex en la web**: tu clon no se actualiza solo. Corre `bash scripts/sincronizar.sh` al empezar **cada turno**.

## 3. Convenciones

- **Todo en español**: UI, comentarios, commits, docs. Lenguaje simple, sin jerga, pensando también en principiantes.
- **Celular primero**: una columna de máx. 480 px, operable con el pulgar.
- **Tema claro fijo** (`:root`); el oscuro solo con `data-theme="dark"`.
- **El prototipo es un archivo único a propósito** (se publica tal cual como página). Todo inline, sin dependencias externas salvo Google Fonts.
- Colores como variables CSS en `:root` (`--accent`, `--ok`, `--bad`, `--heat-0/1`…). No metas colores sueltos.
- Después de tocar `data/`, `python3 scripts/validar_datos.py`.
- La PWA real va en una carpeta nueva `app/` (no reemplaza a `prototipo/`, que queda como referencia de UI).

## 4. Trampas conocidas

| Trampa | Regla |
|---|---|
| La línea `const IMG = {...}` del prototipo pesa ~270 KB | No la leas ni la pegues entera. Búscala por nombre o edita con un script. |
| El prototipo no usa `data/` | Sus `EX` y `DAY` son ejemplos. La PWA real tiene que leer `data/ejercicios.json` y `data/musculos.json`. |
| `docs/contexto-app-entrenamiento.md` tiene la regla de progresión vieja | Manda `DECISIONES.md` (regla del 2026-11-24). |
| `app/catalogo.js` es generado | Si cambias `data/`, corre `python3 scripts/armar_catalogo.py`. No lo edites a mano. |
| `app/index.html` nació del prototipo | Los cambios de UI se hacen en `app/`; el prototipo ya no es la app. |
| Hay una versión publicada del prototipo (artifact de Claude) | Si la editas, que `prototipo/index.html` quede idéntico. Lee la versión publicada antes de republicar, porque Italo puede haberla cambiado. |
| Fotos de openGym aparecen en su repo junto al texto | Nunca las copies ni las enlaces. |
| `lista-150-ejercicios.csv` lleva BOM | Consérvalo, si no Excel muestra mal los acentos. |
| El repo es público | Nada personal ni secreto. |

## 5. Vocabulario

- **Slot**: hueco de la rutina definido por patrón de movimiento, con 3 alternativas A/B/C.
- **RIR**: repeticiones en reserva. RIR 0 = fallo.
- **Compuesto / aislado**: varias articulaciones (sentadilla, remo) vs. un músculo (curl, laterales).
- **Serie dura**: a RIR 0-3, la que cuenta para el volumen.
- **Conteo ponderado**: principal suma 1, secundario 0,5.
- **Día 4 de rescate**: día flexible que completa lo que faltó en la semana.
- **Biserie**: dos slots seguidos sin descanso entre ellos. **Drop set**: bajar el peso y seguir en la misma serie.
