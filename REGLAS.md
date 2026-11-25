# REGLAS.md · obligatorio, sin excepciones

> Se lee **entero y primero** en cualquier sesión, antes de tocar nada (antes incluso que `AGENTS.md`). Es corto a propósito.
>
> Este repo lo trabajan **varios chats de IA en paralelo** (varios hilos de Claude, y quizás ChatGPT/Codex u otra persona con su IA). Ninguno ve lo que hace el otro en tiempo real. No hay bloqueo ni aviso automático. Estas reglas, `git log`, `DECISIONES.md` y `BITACORA.md` son la única forma de no pisarse ni contradecirse.

---

## Al empezar cualquier sesión, en este orden

1. **`git log -n 15`** en `main`. Los commits de Claude salen firmados `Claude <noreply@anthropic.com>`. Los de Codex/ChatGPT pueden salir con el nombre del usuario, por eso llevan el prefijo `codex:` (u otro que diga qué IA fue). Si hay un commit reciente que no es tuyo, **lee su mensaje completo**.
2. **Lee `DECISIONES.md` entero.** Es lo vigente. Lo que está ahí no se cambia por iniciativa propia.
3. **Lee `BITACORA.md`** desde "En curso" y "Pendientes abiertos" hasta las últimas entradas.
4. **Trae tu rama al día** con `bash scripts/sincronizar.sh` antes del primer cambio. Trabajar sobre una copia vieja es la forma más común de pisar el trabajo de otro.

## Antes de cambiar algo

5. **Revisa "En curso" en `BITACORA.md`.** Si otro hilo está trabajando en lo mismo (mismo archivo o misma función, de hoy o ayer), **pregúntale al usuario** antes de seguir. No asumas que el camino está libre.
6. **Anótate en "En curso"**: una línea con fecha, quién (nombre del hilo o de la IA), rama y qué vas a tocar. Commitea y pushea esa línea a `main` antes de empezar si el trabajo va a durar más de una sesión.
7. **Si el usuario pide algo que contradice `DECISIONES.md`**, no lo hagas en silencio: dile qué decisión choca y pregúntale si la cambia. Si dice que sí, actualiza `DECISIONES.md` (con fecha) y agrega la entrada en la bitácora. Así el próximo chat no "corrige" de vuelta lo que el usuario pidió.

## Mientras trabajas

8. **Una rama por tarea**, que sale de `main` y vuelve a `main`. No se acumulan ramas vivas: se fusiona y se borra.
9. **No dejes un cambio a medias.** Si no se puede terminar, escribe en la bitácora qué falta, por qué se cortó y cuál es el paso siguiente. La próxima sesión puede ser otra IA sin tu contexto.
10. **Nunca reescribas historia compartida**: nada de `push --force`, `commit --amend` sobre algo subido ni `reset --hard` contra el remoto.
11. **Antes de dar algo por terminado**: `bash scripts/verificar.sh` tiene que terminar en `TODO OK`.

## Antes de cerrar cualquier sesión que cambió algo

12. **Agrega una entrada a `BITACORA.md`** (arriba de todo): fecha · quién · qué se hizo · qué queda pendiente · commit.
13. **Sácate de "En curso"** y actualiza "Pendientes abiertos".
14. **Actualiza `DECISIONES.md`** si se decidió algo nuevo, y **`MAPA.md`** si cambió la estructura o una función importante.
15. **Commitea y pushea.** Un cambio que queda solo en tu sesión no existe para los demás.

## La bitácora es de solo agregar

Nunca se edita ni se borra una entrada vieja, ni siquiera la propia. Si algo quedó mal, se agrega una entrada nueva que lo corrige. Las únicas secciones que sí se editan son **"En curso"** y **"Pendientes abiertos"**, porque son estado actual, no historia.

## Datos privados y secretos

- La rutina, metas corporales y registros personales de Italo **no van al repo**.
- URLs de Apps Script, IDs de planillas, tokens y claves **no van al repo**. `scripts/verificar.sh` revisa lo más obvio.
- **Ojo: el repo hoy es público en GitHub.** Todo lo que se sube se puede ver.
