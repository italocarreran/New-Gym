// Service worker: deja la app usable sin señal en el gimnasio.
// - Archivos de la app: primero la red (para recibir arreglos al tiro) y, si no hay señal
//   o tarda más de 3 s, la copia guardada.
// - Fotos de ejercicios y fuentes: la copia guardada primero (no cambian).
// - Supabase no pasa por acá: la capa de datos ya guarda todo en el celular.
const VERSION = '__VERSION__';
const APP = `gym-app-${VERSION}`;
const FOTOS = 'gym-fotos-1';
const BASE = [
  './', 'index.html', 'catalogo.js', 'config.js', 'manifest.webmanifest',
  'datos/index.js', 'datos/local.js', 'datos/remoto.js',
  'iconos/icono-192.png', 'iconos/icono-512.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(APP);
    // uno por uno: si falta config.js (copia local sin Supabase) no se cae todo
    await Promise.all(BASE.map((u) => c.add(new Request(u, { cache: 'reload' })).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('gym-app-') && k !== APP) await caches.delete(k);
    await self.clients.claim();
  })());
});

const conTiempo = (p, ms) => new Promise((ok, mal) => { const t = setTimeout(() => mal(new Error('lento')), ms); p.then((r) => { clearTimeout(t); ok(r); }, (e) => { clearTimeout(t); mal(e); }); });

async function redPrimero(req) {
  const c = await caches.open(APP);
  const red = fetch(req).then((r) => { if (r.ok) c.put(req, r.clone()); return r; });
  try { return await conTiempo(red, 3000); }
  catch {
    const g = await c.match(req, { ignoreSearch: true }) || (req.mode === 'navigate' ? await c.match('index.html') : null);
    if (g) return g;
    return red; // no hay copia: que espere a la red
  }
}

async function guardadoPrimero(req) {
  const c = await caches.open(FOTOS);
  const g = await c.match(req.url);
  if (g) return g;
  // las fotos de GitHub y Google Fonts permiten CORS: se guardan como respuesta normal (no opaca)
  const r = await fetch(req.url, { mode: 'cors', credentials: 'omit' }).catch(() => fetch(req));
  if (r.ok || r.type === 'opaque') c.put(req.url, r.clone());
  return r;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.origin === self.location.origin) { e.respondWith(redPrimero(req)); return; }
  if (u.hostname === 'raw.githubusercontent.com' || u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com') {
    e.respondWith(guardadoPrimero(req));
  }
});
