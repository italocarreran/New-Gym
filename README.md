# New Gym

App personal de registro y orientación en el gimnasio. Pensada para un gimnasio lleno: cuando una máquina está ocupada, la app te da la alternativa equivalente al toque (y te explica por qué sirve), cuenta tus series duras por músculo en la semana y te dice cuándo subir peso.

Uso personal, sin publicidad ni pagos, en español.

## Qué hace (o hará)

- **Rutina por slots con alternativas A/B/C.** Cada slot es un patrón de movimiento ("press pesado", "tirón vertical") con 3 ejercicios equivalentes ordenados. Si A está ocupado, vas a B sin pensar.
- **Reemplazo explicado**: por qué la alternativa es equivalente y cómo ajustar el peso.
- **Registro rápido** de peso, repeticiones y RIR (repeticiones en reserva) por serie, con la sesión anterior a la vista y la meta de hoy.
- **Conteo semanal ponderado** de series por músculo (principal = 1, secundario = 0,5) y mapa de calor del cuerpo.
- **Progresión guiada** (regla en [`DECISIONES.md`](DECISIONES.md)).
- Drop sets, biseries, cronómetro, descanso con barra, técnica por ejercicio.

## Estado

Hoy existe un **prototipo interactivo** completo (`prototipo/index.html`) con datos de ejemplo. La PWA real todavía no está empezada. Ver [`ROADMAP.md`](ROADMAP.md).

## Stack (decidido)

| Parte | Tecnología |
|---|---|
| App | HTML + JS sin framework, como PWA (se instala desde el navegador del celular) |
| Datos | Google Sheets en el Drive del usuario, vía Google Apps Script (planilla visible y editable como respaldo) |
| Hosting | Cloudflare Pages (GitHub Pages no sirve gratis con repo privado) |
| Scripts de datos | Python 3, sin dependencias externas |

## Si eres una IA (o una persona) que llega al repo

Este repo lo trabajan varios chats de IA en paralelo. Para no pisarse ni contradecirse:

| Quieres… | Lee |
|---|---|
| saber las reglas de trabajo (obligatorio, primero) | [`REGLAS.md`](REGLAS.md) |
| saber qué está decidido hoy | [`DECISIONES.md`](DECISIONES.md) |
| saber quién está en qué, qué falta y qué se hizo | [`BITACORA.md`](BITACORA.md) |
| saber cómo se trabaja y las trampas conocidas | [`AGENTS.md`](AGENTS.md) |
| encontrar un archivo o una función | [`MAPA.md`](MAPA.md) |
| ver el plan por etapas | [`ROADMAP.md`](ROADMAP.md) |
| los requisitos originales | [`docs/contexto-app-entrenamiento.md`](docs/contexto-app-entrenamiento.md) |

## Estructura

```
REGLAS.md · DECISIONES.md · BITACORA.md · AGENTS.md (CLAUDE.md) · MAPA.md · ROADMAP.md
prototipo/index.html   prototipo interactivo (un solo archivo)
data/                  catálogo de ejercicios, músculos, fuentes de terceros, lista de íconos
docs/                  requisitos, evaluación de fuentes, capturas
scripts/               sincronizar.sh, verificar.sh, validar_datos.py, importar_opengym.py
herramientas/iconos/   prototipo del generador de íconos
```

Detalle en [`MAPA.md`](MAPA.md).

## Cómo correrlo

**Prototipo:** abre `prototipo/index.html` en el navegador. No necesita servidor ni internet (salvo las fuentes de Google). Para verlo como en el celular, usa el modo responsive del navegador (~390 px de ancho).

**Antes de entregar un cambio:**

```bash
bash scripts/sincronizar.sh   # trae main al día
bash scripts/verificar.sh     # tiene que decir TODO OK
```

**Regenerar la biblioteca de openGym** (solo si se actualiza la fuente):

```bash
git clone https://github.com/DuarteSantos8/openGym /tmp/openGym
python3 scripts/importar_opengym.py /tmp/openGym
```

## Deploy

Todavía no hay deploy. Plan: conectar este repo a Cloudflare Pages (sin paso de build, carpeta de salida = la carpeta de la PWA) y un Apps Script publicado como web app que lea y escriba la planilla. Los secretos (URL del Apps Script, IDs de planilla) **no van al repo**.

## Licencias de datos

- free-exercise-db: dominio público (Unlicense), incluidas las fotos.
- openGym: solo texto (AGPL-3.0 / MIT). **Sus imágenes no se usan.**
- Detalle en [`data/fuentes/LEEME.md`](data/fuentes/LEEME.md) y [`docs/fuentes-de-datos.md`](docs/fuentes-de-datos.md).
