# BITÁCORA · registro de sesiones

> **Solo se agrega.** Nunca se edita ni se borra una entrada vieja, ni siquiera la propia; si algo quedó mal, se agrega una entrada nueva que lo corrige (ver `REGLAS.md`). Entradas nuevas arriba.
>
> Las únicas secciones que sí se editan son **"En curso"** y **"Pendientes abiertos"**, porque son el estado de hoy, no historia.
>
> Formato de entrada: `## fecha · quién · tema`, luego qué se hizo, qué queda pendiente y el commit. Lo decidido va además a `DECISIONES.md`.

---

## En curso

Quién está trabajando en qué ahora mismo. Anótate antes de empezar y sácate al terminar. Si vas a tocar lo mismo que alguien de esta lista, pregúntale al usuario primero.

| Desde | Quién | Rama | Qué toca |
|---|---|---|---|
| 2026-11-25 | Hilo Claude "Planificar app personal de gimnasio" | `claude/project-thread-ly2hj8` | `prototipo/index.html` (todo salvo el dibujo del muñeco) |

Desde ahora esas ramas tienen que salir de `main` y volver a `main` (ver `REGLAS.md` 8).

## Pendientes abiertos

- [ ] **Feedback de Italo sobre el prototipo y el mapa de calor** (2026-11-25).
- [ ] **Estilo de íconos** (2026-11-25): pipeline propio, ChatGPT o compra. Si es Gymvisual, falta que confirmen **por escrito** que se pueden editar y usar con IA.
- [ ] **Empezar la PWA real** en `app/` cuando Italo dé el visto bueno al prototipo (ver `ROADMAP.md`).
- [ ] **Hacer `main` la rama por defecto en GitHub** (Settings → General → Default branch). Hoy GitHub sigue mostrando una rama `claude/*`.
- [ ] **Decidir si el repo vuelve a privado.** Hoy es público.

---

## 2026-11-25 · Claude (hilo "Rediseñar mapa de calor muscular") · nuevo muñeco del mapa de calor

- Muñeco nuevo según el modelo de Italo: figura musculosa de frente y espalda, piel durazno `#F6CBA8` con contorno café `#B5714A`, cada músculo como región propia (`bodyFigure`, `FRONT`, `BACK`; `REGION_GRUPO` dice qué grupo de la app pinta cada región). Incluye abdomen, oblicuos, antebrazo, lumbar y aductores aunque el prototipo aún no los mide.
- Pedidos de Italo en comentarios: sin series hechas, los músculos que tocan hoy solo llevan borde rojo suave (`#D2604E`) y el relleno pasa de piel a rojo según el avance; muñeco del encabezado sin recuadro.
- Tema claro fijo: se quitó el `@media (prefers-color-scheme: dark)`; el oscuro queda solo con `data-theme="dark"`.
- Todo esto ya está en `main` (llegó vía `ly2hj8` y la versión publicada). Nada pendiente de este hilo.

## 2026-11-25 · Claude (hilo "Ordenar repo y documentar para IA") · repo ordenado en `main`

- Se creó `main` juntando el prototipo (rama `claude/project-thread-ly2hj8`, idéntico a la versión publicada) y los datos de ejercicios (rama `claude/project-thread-cj030d`). La rama `claude/project-thread-j37w1e` no se fusionó: su contenido ya estaba superado por `ly2hj8`.
- Documentación con el mismo esquema que los otros repos de Italo (Abby, Balance_SSCC): `REGLAS.md`, `DECISIONES.md`, `AGENTS.md` (+ `CLAUDE.md`), `MAPA.md`, esta bitácora y `ROADMAP.md`.
- Scripts nuevos: `scripts/sincronizar.sh` y `scripts/verificar.sh`.
- Se sumaron los requisitos originales (`docs/contexto-app-entrenamiento.md`, sin la rutina ni las metas personales) y el prototipo del generador de íconos (`herramientas/iconos/`).
- Las entradas de abajo se reconstruyeron de la historia del proyecto para que la bitácora parta completa.
- Pendiente: los de arriba (rama por defecto, visibilidad del repo).

## 2026-11-25 · Claude (hilo "Rediseñar mapa de calor muscular") · muñeco nuevo

- Figura musculosa frente y espalda según el modelo de Italo; músculos de hoy parten solo con borde y se pintan con el avance; sin recuadro en el encabezado. Captura en `docs/img/mapa-calor.png`. (commits `809e196`…`ba2cc77`)

## 2026-11-25 · Claude (hilo "Planificar app personal de gimnasio") · mejoras del prototipo

- Tema claro fijo. Técnica por ejercicio (tres puntitos), drop sets, biseries, descanso con barra y ±15 s, agregar ejercicio entre slots, deslizar para borrar que sigue al dedo, sin mensaje cuando la serie sale bien. (commits `3e90675`…`a03d029`)

## 2026-11-25 · Claude (hilo de íconos) · íconos e imágenes

- Prototipo de íconos propios: fotos de free-exercise-db → MediaPipe Pose → ángulos → SVG plano → GIF de 2 cuadros. MediaPipe falla en poses acostadas y con brazos tras la nuca; se corrige con reglas por ejercicio. Código en `herramientas/iconos/`, muestra en `docs/img/iconos-muestra.png`.
- Cotización: Gymvisual ~USD 0,75 c/u desde 10 (150 ≈ USD 112, perpetua, falta confirmar permiso de edición/IA); exerciseimages.com USD 169 pago único, permite modificar. WorkoutLabs, RepDB y Exercise Animatic prohíben usarlas como input de IA.

## 2026-11-24 · Claude · regla de progresión nueva

- Italo reemplazó "todas las series al tope" por la regla de la última serie con RIR 1-2 (detalle en `DECISIONES.md`). El prototipo la aplica en `plan()` / `progressionNote()`.

## 2026-11-24 · Claude (hilo "Reunir base de datos de ejercicios") · lista de 150 ejercicios

- `data/iconos/lista-150-ejercicios.csv`: 56 del catálogo + 94 comunes, con fotos de referencia verificadas. Sin foto en free-exercise-db: elevaciones laterales en máquina, hip thrust en máquina, sentadilla péndulo. Italo prueba hacer los íconos con ChatGPT usando esas fotos solo como referencia de postura. (commits `f2205da`, `82beb0f`)

## 2026-11-24 · Claude (hilo "Planificar app personal de gimnasio") · ajustes de UI

- Encabezado fijo con cronómetro y muñeco, slots abiertos por defecto, mantener apretado para mover, "Detalles" discreto, fotos animadas, kg/lb por slot. (commits `11be03d`…`678ceae`)

## 2026-11-23 · Claude (hilo "Reunir base de datos de ejercicios") · fuentes de datos

- Catálogo curado de 57 ejercicios, copia de free-exercise-db, texto de openGym (5.632 ejercicios en español, sin imágenes), validador. Evaluación completa en `docs/fuentes-de-datos.md`. A pedido de Italo se sacaron su rutina y sus metas de los datos. (commits `2b927f2`, `ca4a8db`, `ec42726`)

## 2026-11-23 · Claude (hilo "Planificar app personal de gimnasio") · stack y prototipo

- Italo delegó el stack: HTML/JS PWA + Google Sheets/Apps Script + Cloudflare Pages. Se hizo primero un prototipo interactivo para ver cómo se usa antes del código definitivo, con editor de rutina. (commits `ac422fb`, `e57a7db`)
