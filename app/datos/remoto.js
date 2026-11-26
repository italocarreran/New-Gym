// Cliente mínimo de Supabase, sin dependencias.
// Habla directo con dos servicios de Supabase por HTTP:
//   - /auth/v1  → cuentas (crear, entrar, renovar la sesión, salir)
//   - /rest/v1  → tablas (leer y guardar filas)
// Solo usa la clave pública (anon o publishable). Nunca pongas acá la clave secreta.

const MARGEN_RENOVAR = 60; // segundos antes de que venza el pase para renovarlo

export class ErrorRemoto extends Error {
  constructor(mensaje, estado, detalle) {
    super(mensaje);
    this.estado = estado;   // código HTTP (0 = sin conexión)
    this.detalle = detalle;
  }
}

export function crearRemoto({ url, clave, guardarPase, leerPase }) {
  const base = url.replace(/\/+$/, '');

  async function pedir(ruta, { metodo = 'GET', cuerpo, pase, cabeceras = {} } = {}) {
    const h = { apikey: clave, ...cabeceras };
    if (pase) h.Authorization = `Bearer ${pase.access_token}`;
    if (cuerpo !== undefined) h['Content-Type'] = 'application/json';
    let r;
    try {
      r = await fetch(base + ruta, {
        method: metodo,
        headers: h,
        body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
      });
    } catch (e) {
      throw new ErrorRemoto('Sin conexión con Supabase', 0, e);
    }
    const texto = await r.text();
    let datos = null;
    if (texto) { try { datos = JSON.parse(texto); } catch { datos = texto; } }
    if (!r.ok) {
      const m = (datos && (datos.msg || datos.message || datos.error_description || datos.error)) || r.statusText;
      throw new ErrorRemoto(String(m), r.status, datos);
    }
    return datos;
  }

  function aPase(d) {
    if (!d || !d.access_token) return null;
    return {
      access_token: d.access_token,
      refresh_token: d.refresh_token,
      expires_at: d.expires_at || Math.floor(Date.now() / 1000) + (d.expires_in || 3600),
      usuario: { id: d.user.id, email: d.user.email },
    };
  }

  // ---- Cuentas ----------------------------------------------------------

  async function crearCuenta(email, clave_) {
    const d = await pedir('/auth/v1/signup', { metodo: 'POST', cuerpo: { email, password: clave_ } });
    const pase = aPase(d);
    if (pase) await guardarPase(pase);
    // Si Supabase pide confirmar el correo, no llega pase todavía.
    return { pase, confirmarCorreo: !pase };
  }

  async function entrar(email, clave_) {
    const d = await pedir('/auth/v1/token?grant_type=password', {
      metodo: 'POST', cuerpo: { email, password: clave_ },
    });
    const pase = aPase(d);
    await guardarPase(pase);
    return pase;
  }

  async function salir() {
    const pase = await leerPase();
    await guardarPase(null);
    if (pase) { try { await pedir('/auth/v1/logout', { metodo: 'POST', pase }); } catch { /* da igual */ } }
  }

  // Devuelve un pase vigente, renovándolo si está por vencer. null si no hay sesión.
  let renovando = null;
  async function paseVigente() {
    const pase = await leerPase();
    if (!pase) return null;
    if (pase.expires_at - MARGEN_RENOVAR > Date.now() / 1000) return pase;
    if (!renovando) {
      renovando = (async () => {
        try {
          const d = await pedir('/auth/v1/token?grant_type=refresh_token', {
            metodo: 'POST', cuerpo: { refresh_token: pase.refresh_token },
          });
          const nuevo = aPase(d);
          await guardarPase(nuevo);
          return nuevo;
        } catch (e) {
          // Pase rechazado (no es falta de señal): hay que volver a entrar.
          if (e.estado >= 400 && e.estado < 500) await guardarPase(null);
          throw e;
        } finally {
          renovando = null;
        }
      })();
    }
    return renovando;
  }

  // ---- Tablas -----------------------------------------------------------

  // Sube filas; si el id ya existe, la actualiza (la base decide cuál versión gana).
  async function subir(tabla, filas) {
    const pase = await paseVigente();
    if (!pase) throw new ErrorRemoto('No hay sesión iniciada', 401);
    await pedir(`/rest/v1/${tabla}?on_conflict=id`, {
      metodo: 'POST', cuerpo: filas, pase,
      cabeceras: { Prefer: 'resolution=merge-duplicates,return=minimal' },
    });
  }

  // Baja las filas que llegaron a la base después de `desde` (texto ISO).
  async function bajar(tabla, desde, limite = 1000, salto = 0) {
    const pase = await paseVigente();
    if (!pase) throw new ErrorRemoto('No hay sesión iniciada', 401);
    const q = `select=*&order=servidor_en.asc,id.asc&limit=${limite}&offset=${salto}` +
      (desde ? `&servidor_en=gt.${encodeURIComponent(desde)}` : '');
    return pedir(`/rest/v1/${tabla}?${q}`, { pase });
  }

  return { crearCuenta, entrar, salir, paseVigente, subir, bajar };
}
