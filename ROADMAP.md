# Roadmap

Estado al 2026-11-25. Plan por etapas. Lo inmediato (y quién está en qué) vive en `BITACORA.md`; al terminar algo, márcalo con `[x]` acá y anótalo en la bitácora.

## Ahora

- [ ] Recibir feedback de Italo sobre el prototipo y el mapa de calor.
- [ ] Decidir el estilo de íconos: pipeline propio (MediaPipe), íconos hechos con ChatGPT, o comprar (Gymvisual si confirman permiso por escrito; exerciseimages.com como respaldo).

## PWA real (versión 1)

- [ ] Carpeta `app/` con la PWA: `index.html`, `manifest.webmanifest`, service worker para que funcione sin internet en el gimnasio.
- [ ] Pasar la UI del prototipo a la app, leyendo `data/ejercicios.json` y `data/musculos.json` en vez de los datos de ejemplo (`EX`, `DAY`).
- [ ] App en blanco: el usuario arma sus días y slots en Editar.
- [ ] Registro de series (ejercicio usado, posición en la sesión, peso, reps, RIR, drop sets).
- [ ] Regla de progresión completa (ver bitácora), con sesión anterior y meta de hoy.
- [ ] Conteo semanal ponderado con metas que define el usuario, y aviso del músculo atrasado.
- [ ] Sugerencia del día 4 de rescate.
- [ ] Recorte por falta de tiempo según prioridad del slot.
- [ ] Sugerencia de ejercicio de relleno mientras se espera una máquina.

## Backend en Google Sheets

- [ ] Planilla con hojas: `rutina`, `registros`, `ajustes`.
- [ ] Apps Script publicado como web app (leer/escribir). La URL va como secreto, no en el repo.
- [ ] Guardado local primero y sincronización cuando haya señal.

## Deploy

- [ ] Conectar el repo a Cloudflare Pages (sin build, carpeta `app/`).
- [ ] Instalar en el celular como ícono de inicio.

## Después

- [ ] Gráficos de progresión por ejercicio y por músculo.
- [ ] Semana liviana cada 5-6 semanas.
- [ ] Peso corporal y % de grasa (balanza Fitdays).
- [ ] Íconos propios para los 150 ejercicios.
- [ ] Copiar las fotos de free-exercise-db al repo para no depender de GitHub.
