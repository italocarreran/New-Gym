// Capa de datos de la App GYM. Es lo ÚNICO que el resto de la app usa para
// leer y guardar. La app no sabe si detrás hay Supabase, Sheets u otra cosa.
//
//   import { crearDatos } from './datos/index.js';
//   const datos = await crearDatos(window.GYM_CONFIG);
//
// Todo se guarda primero en el celular (funciona sin señal) y se sube solo a
// Supabase cuando hay conexión y sesión iniciada. Ver datos/LEEME.md.

import { abrirLocal, adoptarInvitado, TABLAS } from './local.js';
import { crearRemoto } from './remoto.js';

const ESPERA_SUBIR_MS = 2000;            // tras un cambio, espera un poco y sube
const CADA_MS = 5 * 60 * 1000;           // y además revisa cada 5 minutos
const SOLAPE_MS = 2 * 60 * 1000;         // al bajar, repasa 2 min hacia atrás por si algo llegó tarde
const LOTE = 200;
const PAGINA = 1000;
const FECHAS = ['inicio', 'fin', 'hecha_en', 'creado_en', 'actualizado_en', 'servidor_en'];
const CLAVE_PASE = 'gym-pase';

const ahora = () => new Date().toISOString();
const nuevoId = () => crypto.randomUUID();
const vivas = (filas) => filas.filter((f) => !f.borrado);
// Supabase devuelve fechas como "2026-11-26T10:00:00+00:00"; acá todas van como "…Z"
// para poder ordenarlas y compararlas como texto.
const normalizar = (f) => {
  const r = { ...f };
  for (const c of FECHAS) if (r[c]) r[c] = new Date(r[c]).toISOString();
  return r;
};
const limpiar = (f) => { const { _pendiente, user_id, ...resto } = f; return resto; };

export async function crearDatos({ url, clave, idb = globalThis.indexedDB, almacen = globalThis.localStorage } = {}) {
  const conNube = Boolean(url && clave);
  const leerPase = async () => { try { return JSON.parse(almacen.getItem(CLAVE_PASE)); } catch { return null; } };
  const guardarPase = async (p) => { if (p) almacen.setItem(CLAVE_PASE, JSON.stringify(p)); else almacen.removeItem(CLAVE_PASE); };
  const remoto = conNube ? crearRemoto({ url, clave, leerPase, guardarPase }) : null;

  let local = null;
  let usuario = null;
  const oyentes = new Set();
  const estado = { nube: conNube, sincronizando: false, ultimaSync: null, error: null, pendientes: 0, debeEntrar: false };

  async function avisar() {
    estado.pendientes = local ? await local.contarPendientes() : 0;
    for (const f of oyentes) { try { f({ ...estado, usuario }); } catch (e) { console.error(e); } }
  }

  async function usarBase(u) {
    if (local) local.cerrar();
    usuario = u;
    local = await abrirLocal(u ? `gym-${u.id}` : 'gym-invitado', idb);
    estado.ultimaSync = await local.leerMeta('ultimaSync');
  }

  const pase = await leerPase();
  await usarBase(pase ? pase.usuario : null);

  // ---- Guardado genérico ------------------------------------------------

  let temporizador = null;
  function programarSubida() {
    clearTimeout(temporizador);
    temporizador = setTimeout(() => { sincronizar().catch(() => {}); }, ESPERA_SUBIR_MS);
  }

  async function guardar(tabla, fila) {
    const f = { ...fila, actualizado_en: ahora(), _pendiente: 1 };
    if (!f.creado_en) f.creado_en = f.actualizado_en;
    if (f.borrado === undefined) f.borrado = false;
    await local.poner(tabla, f);
    await avisar();
    programarSubida();
    return limpiar(f);
  }

  async function cambiar(tabla, id, cambios) {
    const actual = await local.una(tabla, id);
    if (!actual) throw new Error(`No existe ${tabla} ${id}`);
    return guardar(tabla, { ...actual, ...cambios, id });
  }

  const borrar = (tabla, id) => cambiar(tabla, id, { borrado: true });

  // ---- Sincronización ---------------------------------------------------

  let enCurso = null;
  function sincronizar() {
    if (!remoto || !usuario) return Promise.resolve(false);
    if (globalThis.navigator && navigator.onLine === false) return Promise.resolve(false);
    if (!enCurso) {
      enCurso = (async () => {
        estado.sincronizando = true; estado.error = null; await avisar();
        try {
          for (const t of TABLAS) {
            // 1) Subir lo anotado acá.
            const pend = await local.pendientes(t);
            for (let i = 0; i < pend.length; i += LOTE) {
              const lote = pend.slice(i, i + LOTE);
              await remoto.subir(t, lote.map(limpiar));
              await local.marcarSubidas(t, lote);
            }
            // 2) Bajar lo que llegó desde otros aparatos (por páginas).
            const cursor = await local.leerMeta(`cursor-${t}`);
            const desde = cursor ? new Date(Date.parse(cursor) - SOLAPE_MS).toISOString() : null;
            let maximo = cursor;
            for (let salto = 0; ; salto += PAGINA) {
              const filas = (await remoto.bajar(t, desde, PAGINA, salto)).map(normalizar);
              if (filas.length) {
                await local.mezclarBajadas(t, filas);
                const ultimo = filas[filas.length - 1].servidor_en;
                if (!maximo || ultimo > maximo) maximo = ultimo;
              }
              if (filas.length < PAGINA) break;
            }
            if (maximo !== cursor) await local.guardarMeta(`cursor-${t}`, maximo);
          }
          estado.ultimaSync = ahora();
          await local.guardarMeta('ultimaSync', estado.ultimaSync);
          return true;
        } catch (e) {
          estado.error = e.estado === 0 ? 'Sin conexión' : e.message;
          // Pase vencido o rechazado: lo anotado sigue en el celular y sube al volver a entrar.
          estado.debeEntrar = !(await leerPase());
          return false;
        } finally {
          estado.sincronizando = false; enCurso = null; await avisar();
        }
      })();
    }
    return enCurso;
  }

  if (globalThis.addEventListener) {
    addEventListener('online', () => sincronizar());
    if (globalThis.document) {
      document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') sincronizar(); });
    }
  }
  setInterval(() => sincronizar(), CADA_MS);

  // ---- Cuenta -----------------------------------------------------------

  async function alEntrar(p) {
    const invitado = await abrirLocal('gym-invitado', idb);
    if (local) local.cerrar();
    local = null;
    usuario = p.usuario;
    local = await abrirLocal(`gym-${usuario.id}`, idb);
    await adoptarInvitado(invitado, local, usuario.id, idb);
    estado.debeEntrar = false; estado.error = null;
    estado.ultimaSync = await local.leerMeta('ultimaSync');
    await avisar();
    sincronizar();
    return usuario;
  }

  const cuenta = {
    usuario: () => usuario,
    async crear(email, contrasena) {
      if (!remoto) throw new Error('Falta configurar Supabase (config.js)');
      const r = await remoto.crearCuenta(email, contrasena);
      if (r.pase) await alEntrar(r.pase);
      return { confirmarCorreo: r.confirmarCorreo };
    },
    async entrar(email, contrasena) {
      if (!remoto) throw new Error('Falta configurar Supabase (config.js)');
      return alEntrar(await remoto.entrar(email, contrasena));
    },
    // Lo que no alcanzó a subir queda guardado en el celular y sube al volver a entrar.
    async salir() {
      if (remoto) await remoto.salir();
      await usarBase(null);
      await avisar();
    },
  };

  // ---- Rutinas ----------------------------------------------------------

  const rutinas = {
    async listar() {
      return vivas(await local.todas('rutinas')).sort((a, b) => a.orden - b.orden).map(limpiar);
    },
    obtener: async (id) => { const r = await local.una('rutinas', id); return r && !r.borrado ? limpiar(r) : null; },
    // { id?, nombre, orden?, slots }
    guardar: (r) => guardar('rutinas', { orden: 0, slots: [], ...r, id: r.id || nuevoId() }),
    borrar: (id) => borrar('rutinas', id),
  };

  // ---- Sesiones ---------------------------------------------------------

  const sesiones = {
    iniciar: ({ rutina_id = null, rutina_nombre = null, inicio = ahora() } = {}) =>
      guardar('sesiones', { id: nuevoId(), rutina_id, rutina_nombre, inicio, fin: null, notas: null }),
    terminar: (id, { notas } = {}) => cambiar('sesiones', id, { fin: ahora(), ...(notas !== undefined ? { notas } : {}) }),
    cambiar: (id, cambios) => cambiar('sesiones', id, cambios),
    borrar: (id) => borrar('sesiones', id),
    obtener: async (id) => { const s = await local.una('sesiones', id); return s && !s.borrado ? limpiar(s) : null; },
    // Sesiones entre dos fechas (texto ISO), de la más nueva a la más vieja.
    async listar({ desde = '', hasta = '￿' } = {}) {
      const filas = await local.porIndice('sesiones', 'inicio', IDBKeyRange.bound(desde, hasta));
      return vivas(filas).sort((a, b) => b.inicio.localeCompare(a.inicio)).map(limpiar);
    },
  };

  // ---- Series -----------------------------------------------------------

  const series = {
    // { sesion_id, ejercicio_id, numero, peso, unidad, reps, rir, slot_id?, opcion?, posicion?, drop_de?, biserie_con?, aviso_orden? }
    agregar(s) {
      if (!s.sesion_id || !s.ejercicio_id || !s.numero) throw new Error('Falta sesion_id, ejercicio_id o numero');
      return guardar('series', {
        unidad: 'kg', peso: null, reps: null, rir: null, slot_id: null, opcion: null, posicion: null,
        drop_de: null, biserie_con: null, aviso_orden: null, hecha_en: ahora(), ...s, id: s.id || nuevoId(),
      });
    },
    cambiar: (id, cambios) => cambiar('series', id, cambios),
    borrar: (id) => borrar('series', id),
    async deSesion(sesionId) {
      const filas = vivas(await local.porIndice('series', 'sesion', sesionId));
      return filas.sort((a, b) => (a.posicion ?? 0) - (b.posicion ?? 0) || a.numero - b.numero).map(limpiar);
    },
    // La última vez que se hizo un ejercicio (sin contar la sesión de hoy):
    // { sesion, series: [...] } o null. Sirve para "sesión anterior" y "meta de hoy".
    async ultimaVez(ejercicioId, { sinSesion = null } = {}) {
      const filas = vivas(await local.porIndice('series', 'ejercicio',
        IDBKeyRange.bound([ejercicioId, ''], [ejercicioId, '￿'])))
        .filter((f) => f.sesion_id !== sinSesion)
        .sort((a, b) => b.hecha_en.localeCompare(a.hecha_en));
      if (!filas.length) return null;
      const sid = filas[0].sesion_id;
      return {
        sesion: await sesiones.obtener(sid),
        series: filas.filter((f) => f.sesion_id === sid).sort((a, b) => a.numero - b.numero).map(limpiar),
      };
    },
    // Todas las series entre dos fechas (para el conteo semanal por músculo).
    async entre(desde, hasta) {
      const filas = vivas(await local.todas('series'));
      return filas.filter((f) => f.hecha_en >= desde && f.hecha_en < hasta).map(limpiar);
    },
  };

  // ---- Ajustes ----------------------------------------------------------

  const ID_AJUSTES = () => (usuario ? usuario.id : 'invitado');
  const ajustes = {
    async leer() { const a = await local.una('ajustes', ID_AJUSTES()); return a ? a.datos : {}; },
    async guardar(cambios) {
      const id = ID_AJUSTES();
      const a = await local.una('ajustes', id);
      return guardar('ajustes', { ...(a || {}), id, datos: { ...(a ? a.datos : {}), ...cambios } });
    },
  };

  await avisar();
  if (usuario) sincronizar();

  return {
    cuenta, rutinas, sesiones, series, ajustes, sincronizar,
    estado: () => ({ ...estado, usuario }),
    // f(estado) se llama cada vez que cambia algo (pendientes, sincronizando, error, usuario).
    alCambiar(f) { oyentes.add(f); return () => oyentes.delete(f); },
  };
}
