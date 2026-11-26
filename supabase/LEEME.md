# Supabase · cómo crear el proyecto

La app guarda el registro (sesiones, series, rutinas y ajustes) en Supabase, plan gratis. Esto lo hace Italo una sola vez; toma unos 10 minutos.

## Pasos

1. Entra a **supabase.com** → **Start your project** → inicia sesión (con GitHub es lo más rápido).
2. **New project**:
   - Organización: la que te crea por defecto (plan **Free**).
   - Nombre: `app-gym`.
   - **Database password**: genera una y guárdala en tu gestor de claves. **No se la pases a nadie**, ni a la IA. La app no la usa.
   - Región: **South America (São Paulo)**, la más cerca de Chile.
   - Create new project. Espera 1-2 minutos a que quede listo.
3. **Crear las tablas**: menú izquierdo → **SQL Editor** → **New query** → pega entero `supabase/esquema.sql` → **Run**. Debe decir "Success. No rows returned". Se puede correr de nuevo sin problema.
4. **Cuentas**: menú → **Authentication** → **Sign In / Providers** → **Email** queda activo (viene así).
   - Para que sea más simple, apaga **Confirm email** (si no, Supabase te manda un correo para confirmar la cuenta antes de poder entrar). Cuando la app tenga más usuarios, se vuelve a prender.
5. **Copiar los dos datos que necesito**: botón **Connect** arriba (o **Project Settings → API Keys** y **Data API**):
   - **Project URL**: algo como `https://abcdefghij.supabase.co`.
   - **Publishable key** (empieza con `sb_publishable_`). Si solo ves claves "legacy", sirve la **anon public**.
   - **Nunca** copies la **Secret key** (`sb_secret_…`) ni la **service_role**: esas abren todo, saltándose los permisos.
6. Pásame la URL y la publishable key en el hilo. No van al repo: van en `app/config.js` (que está en `.gitignore`) y, cuando publiquemos, como variables en Cloudflare Pages.

## Probar que funciona

1. Copia `app/config.ejemplo.js` como `app/config.js` y pon tus dos datos.
2. Desde la carpeta del repo: `python3 -m http.server 8000` y abre `http://localhost:8000/app/datos/prueba.html`.
3. **Crear cuenta** con tu correo y una contraseña, anota una serie y toca **Sincronizar ahora**. En Supabase → **Table Editor → series** debería aparecer la fila.

## Ojo con el plan gratis

- **Se pausa solo tras 7 días sin uso** (sin ninguna consulta). Los datos no se pierden: entras a supabase.com y tocas **Restore project** (tarda unos minutos). Mientras está pausado, la app sigue anotando en el celular y sube todo cuando vuelve.
- Si entrenas al menos una vez por semana, no se pausa. Si quieres evitarlo del todo, se puede agregar un aviso automático semanal (pendiente en `BITACORA.md`).
- Límites gratis: 500 MB de base de datos y 50.000 usuarios al mes. Un registro de gimnasio usa muy poco (años de series caben en unos pocos MB).

## Publicar en Cloudflare Pages (más adelante)

Como `app/config.js` no está en el repo, Cloudflare lo arma al publicar:

- Variables de entorno: `SUPABASE_URL` y `SUPABASE_CLAVE` (la publishable).
- Build command:
  `printf 'window.GYM_CONFIG={url:"%s",clave:"%s"};\n' "$SUPABASE_URL" "$SUPABASE_CLAVE" > app/config.js`
- Output directory: `app`.
- En Supabase → Authentication → **URL Configuration** → **Site URL**: la dirección de Cloudflare (sirve para los correos de confirmación y de cambio de contraseña).
