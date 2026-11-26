# Instalar la app en el celular

La app se publica sola en **GitHub Pages** cada vez que cambia `main` (`.github/workflows/publicar.yml`). Dirección:

**https://italocarreran.github.io/New-Gym/**

## Una sola vez, en GitHub (Italo)

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
2. **Settings → Secrets and variables → Actions → pestaña Variables → New repository variable**, dos veces:
   - `SUPABASE_URL`: la Project URL de Supabase.
   - `SUPABASE_CLAVE`: la **publishable key** (`sb_publishable_…`). Nunca la secret.
   Son públicas por diseño (quedan en `config.js` de la página), pero no se escriben en el repo.
3. **Actions → Publicar app → Run workflow** (solo si el primer intento falló porque Pages no estaba activado).

Sin las variables la app igual funciona: en el celular pide pegar la URL y la clave una vez.

## En el celular (Android, Chrome)

1. Abre la dirección de arriba en Chrome.
2. Menú **⋮ → Instalar app** (o **Agregar a pantalla principal**).
3. Abre la app desde el ícono y **crea tu cuenta** (correo + contraseña). Cada cuenta ve solo sus datos.
4. La primera vez abre cada rutina con señal para que se guarden las fotos. Después funciona sin internet y sube lo anotado cuando vuelve la señal.

En iPhone: Safari → Compartir → **Agregar a inicio**.

## Actualizaciones y bugs

- Cada cambio en `main` se publica en 1-2 minutos. El celular lo toma al abrir la app con señal (si no aparece, ciérrala del todo y ábrela de nuevo).
- La versión instalada sale al final de **Inicio → Cuenta**. Anótala al reportar un bug.

## Si el repo vuelve a ser privado

GitHub Pages deja de ser gratis con repo privado. Se pasa a Cloudflare Pages (ver `supabase/LEEME.md`): mismo `app/`, mismas dos variables.
