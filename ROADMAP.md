# Roadmap

Estado al 2026-11-25. Plan por etapas. Lo inmediato (y quién está en qué) vive en `BITACORA.md`; al terminar algo, márcalo con `[x]` acá y anótalo en la bitácora.

## Ahora

- [ ] Recibir feedback de Italo sobre el prototipo y el mapa de calor.
- [ ] Decidir el estilo de íconos: pipeline propio (MediaPipe), íconos hechos con ChatGPT, o comprar (Gymvisual si confirman permiso por escrito; exerciseimages.com como respaldo).

## PWA real (versión 1)

- [x] Carpeta `app/` con la PWA: `index.html`, `manifest.webmanifest`, service worker para que funcione sin internet en el gimnasio.
- [x] Pasar la UI del prototipo a la app, leyendo `data/` (vía `app/catalogo.js`).
- [x] App en blanco: el usuario arma sus días y slots en Editar.
- [x] Registro de series (ejercicio usado, posición en la sesión, peso, reps, RIR, drop sets).
- [ ] Metas semanales por músculo editables en la app.
- [ ] Regla de progresión completa (ver bitácora), con sesión anterior y meta de hoy.
- [ ] Conteo semanal ponderado con metas que define el usuario, y aviso del músculo atrasado.
- [ ] Sugerencia del día 4 de rescate.
- [ ] Recorte por falta de tiempo según prioridad del slot.
- [ ] Sugerencia de ejercicio de relleno mientras se espera una máquina.

## Datos en Supabase

- [x] Esquema con cuentas y permisos por usuario (`supabase/esquema.sql`).
- [x] Capa de datos con copia local y sincronización (`app/datos/`).
- [x] Italo crea el proyecto Supabase (`supabase/LEEME.md`) y pasa URL + publishable key.
- [x] Conectar las pantallas de la PWA a `app/datos/`.

## Deploy

- [x] Publicación automática en GitHub Pages desde `main` (`.github/workflows/publicar.yml`).
- [ ] Italo activa Pages y agrega las variables (`docs/instalar-en-el-celular.md`).
- [ ] Instalar en el celular como ícono de inicio.

## Después

- [ ] Gráficos de progresión por ejercicio y por músculo.
- [ ] Semana liviana cada 5-6 semanas.
- [ ] Peso corporal y % de grasa (balanza Fitdays).
- [ ] Íconos propios para los 150 ejercicios.
- [ ] Copiar las fotos de free-exercise-db al repo para no depender de GitHub.
