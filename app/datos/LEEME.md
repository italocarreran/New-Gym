# Capa de datos (`app/datos/`)

Lo **único** que la app usa para leer y guardar. Ninguna otra parte de la app habla con Supabase ni con IndexedDB. Si un día se cambia Supabase por otra cosa, se cambia `remoto.js` y nada más.

| Archivo | Qué hace |
|---|---|
| `index.js` | API pública (`crearDatos`) y la sincronización |
| `local.js` | copia local en el celular (IndexedDB), una base por usuario |
| `remoto.js` | cliente mínimo de Supabase por HTTP (cuentas + tablas), sin dependencias |
| `prueba.html` | página para probar cuenta, anotar series y sincronizar |

Las tablas, permisos y triggers están en `supabase/esquema.sql`.

## Cómo se usa

```js
import { crearDatos } from './datos/index.js';
const datos = await crearDatos(window.GYM_CONFIG); // {url, clave}; sin config funciona solo local

await datos.cuenta.entrar(email, contrasena);      // también crear(), salir(), usuario()

const ses = await datos.sesiones.iniciar({ rutina_id, rutina_nombre });
await datos.series.agregar({ sesion_id: ses.id, ejercicio_id: 'press_banca_barra',
  numero: 1, peso: 60, unidad: 'kg', reps: 10, rir: 2, posicion: 1, slot_id: 's1', opcion: 'A' });
await datos.series.cambiar(id, { reps: 9 });
await datos.series.borrar(id);                     // deslizar para borrar
await datos.sesiones.terminar(ses.id);

await datos.series.ultimaVez('press_banca_barra', { sinSesion: ses.id }); // {sesion, series} de la vez anterior
await datos.series.deSesion(ses.id);
await datos.series.entre(desdeISO, hastaISO);      // para el conteo semanal por músculo
await datos.sesiones.listar({ desde, hasta });     // calendario de Inicio

await datos.rutinas.listar() / guardar({ id?, nombre, orden, slots }) / borrar(id);
await datos.ajustes.leer() / guardar({ metas: {...}, unidad: 'kg' });

datos.alCambiar((e) => { /* e.pendientes, e.sincronizando, e.ultimaSync, e.error, e.debeEntrar, e.usuario */ });
```

Todo devuelve al tiro (lee y escribe en el celular). Las fechas van como texto ISO en UTC (`2026-11-26T14:00:00.000Z`).

## Cómo sincroniza

- Cada cambio queda en el celular marcado "pendiente". A los 2 s, al volver la señal, al abrir la app y cada 5 min, se **sube** lo pendiente y se **baja** lo que llegó de otros aparatos.
- Los id los crea el celular, así que subir dos veces la misma serie no la duplica.
- Si dos aparatos editan lo mismo, **gana el cambio más reciente** (lo decide la base con `actualizado_en`).
- Borrar es marcar `borrado = true`; así el borrado también llega a los otros aparatos.
- Sin cuenta se guarda como "invitado". Al entrar, lo del invitado pasa a la cuenta y se sube.
- Si el pase de la cuenta vence sin señal, nada se pierde: se sigue anotando y sube al volver a entrar (`debeEntrar`).

## Probarla

`prueba.html` (ver `supabase/LEEME.md`). La lógica se probó con dos "celulares" simulados contra un Postgres local con el mismo esquema: subida, bajada, conflicto, borrado, invitado → cuenta, paginación con 2.500 series y que un usuario no ve filas de otro.
