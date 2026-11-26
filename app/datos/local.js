// Copia local en el celular (IndexedDB). La app lee y escribe siempre acá,
// tenga o no señal. La sincronización con Supabase va aparte (sincronizar.js).
//
// Cada usuario tiene su propia base local ("gym-<id>"). Antes de iniciar
// sesión se usa "gym-invitado"; al entrar, lo anotado como invitado se pasa
// a la cuenta.

export const TABLAS = ['rutinas', 'sesiones', 'series', 'ajustes'];
const VERSION = 1;

function promesa(req) {
  return new Promise((ok, mal) => {
    req.onsuccess = () => ok(req.result);
    req.onerror = () => mal(req.error);
  });
}

function fin(tx) {
  return new Promise((ok, mal) => {
    tx.oncomplete = () => ok();
    tx.onerror = () => mal(tx.error);
    tx.onabort = () => mal(tx.error);
  });
}

export async function abrirLocal(nombre, idb = globalThis.indexedDB) {
  const req = idb.open(nombre, VERSION);
  req.onupgradeneeded = () => {
    const db = req.result;
    for (const t of TABLAS) {
      if (!db.objectStoreNames.contains(t)) {
        const s = db.createObjectStore(t, { keyPath: 'id' });
        s.createIndex('pendiente', '_pendiente');
        if (t === 'series') {
          s.createIndex('sesion', 'sesion_id');
          s.createIndex('ejercicio', ['ejercicio_id', 'hecha_en']);
        }
        if (t === 'sesiones') s.createIndex('inicio', 'inicio');
      }
    }
    if (!db.objectStoreNames.contains('meta')) db.createObjectStore('meta');
  };
  const db = await promesa(req);

  const api = {
    nombre,

    async todas(tabla) {
      const tx = db.transaction(tabla);
      return promesa(tx.objectStore(tabla).getAll());
    },

    async una(tabla, id) {
      const tx = db.transaction(tabla);
      return (await promesa(tx.objectStore(tabla).get(id))) || null;
    },

    async porIndice(tabla, indice, rango) {
      const tx = db.transaction(tabla);
      return promesa(tx.objectStore(tabla).index(indice).getAll(rango));
    },

    async poner(tabla, filas) {
      const tx = db.transaction(tabla, 'readwrite');
      const s = tx.objectStore(tabla);
      for (const f of [].concat(filas)) s.put(f);
      await fin(tx);
    },

    async pendientes(tabla) {
      return api.porIndice(tabla, 'pendiente', 1);
    },

    async contarPendientes() {
      let n = 0;
      for (const t of TABLAS) {
        const tx = db.transaction(t);
        n += await promesa(tx.objectStore(t).index('pendiente').count(1));
      }
      return n;
    },

    // Marca como subidas solo las filas que no cambiaron mientras se subían.
    async marcarSubidas(tabla, filas) {
      const tx = db.transaction(tabla, 'readwrite');
      const s = tx.objectStore(tabla);
      for (const f of filas) {
        const r = s.get(f.id);
        r.onsuccess = () => {
          const actual = r.result;
          if (actual && actual.actualizado_en === f.actualizado_en) {
            actual._pendiente = 0;
            s.put(actual);
          }
        };
      }
      await fin(tx);
    },

    // Guarda lo que bajó de Supabase, salvo que acá haya una versión más nueva sin subir.
    async mezclarBajadas(tabla, filas) {
      const tx = db.transaction(tabla, 'readwrite');
      const s = tx.objectStore(tabla);
      let cambios = 0;
      for (const remota of filas) {
        const r = s.get(remota.id);
        r.onsuccess = () => {
          const local = r.result;
          if (local && local._pendiente && Date.parse(local.actualizado_en) > Date.parse(remota.actualizado_en)) return;
          s.put({ ...remota, _pendiente: 0 });
          cambios++;
        };
      }
      await fin(tx);
      return cambios;
    },

    async leerMeta(clave) {
      const tx = db.transaction('meta');
      return (await promesa(tx.objectStore('meta').get(clave))) ?? null;
    },

    async guardarMeta(clave, valor) {
      const tx = db.transaction('meta', 'readwrite');
      tx.objectStore('meta').put(valor, clave);
      await fin(tx);
    },

    cerrar() { db.close(); },
  };
  return api;
}

// Pasa todo lo del invitado a la base de la cuenta (como pendiente de subir) y vacía la del invitado.
// Los ajustes son una sola fila por persona: su id es el id de la cuenta.
export async function adoptarInvitado(invitado, cuenta, usuarioId, idb = globalThis.indexedDB) {
  let n = 0;
  for (const t of TABLAS) {
    let filas = await invitado.todas(t);
    if (t === 'ajustes') filas = filas.map((f) => ({ ...f, id: usuarioId }));
    if (!filas.length) continue;
    const ya = new Set((await cuenta.todas(t)).map((f) => f.id));
    const nuevas = filas.filter((f) => !ya.has(f.id)).map((f) => {
      const { user_id, ...resto } = f;
      return { ...resto, _pendiente: 1 };
    });
    if (nuevas.length) await cuenta.poner(t, nuevas);
    n += nuevas.length;
  }
  invitado.cerrar();
  await promesa(idb.deleteDatabase(invitado.nombre));
  return n;
}
