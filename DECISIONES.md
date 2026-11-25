# DECISIONES.md · lo vigente, en un solo lugar

> Esto es lo que está decidido **hoy**. Si algo de otro documento (incluido `docs/contexto-app-entrenamiento.md`) choca con esto, manda esto.
>
> **No se cambia por iniciativa propia.** Solo cuando el usuario lo pide o lo aprueba. Al cambiar algo: se edita acá, se pone la fecha nueva, y se agrega una entrada en `BITACORA.md` que diga qué había antes y por qué cambió (ver `REGLAS.md` 7).
>
> Entre paréntesis: fecha y quién lo decidió.

---

## Producto

- App **personal** de un solo usuario (Italo), en español de Chile. Sin publicidad, sin pagos, no va a tiendas de apps. (Italo, 2026-11-23)
- El problema central: elegir rápido una alternativa equivalente cuando una máquina está ocupada, llevar las series duras por músculo en la semana y saber cuándo subir peso. (Italo, 2026-11-23)
- **La app parte en blanco.** La rutina personal de Italo no va en el repo ni en los datos; él arma, ordena y edita sus días y ejercicios a mano. (Italo, 2026-11-23)
- El foco por ahora es la app; las consultas de series y volumen de su rutina vienen después. (Italo, 2026-11-23)

## Stack

- HTML + JS **sin framework**, como **PWA**. Sin bundlers ni npm salvo que el usuario lo apruebe. (Italo delegó, 2026-11-23)
- Datos en **Google Sheets** vía **Google Apps Script** (planilla visible y editable como respaldo). (2026-11-23)
- Hosting en **Cloudflare Pages** (GitHub Pages no sirve gratis con repo privado). (2026-11-23)
- Scripts de datos en Python 3 sin dependencias. (2026-11-23)
- Rama oficial: **`main`**. (Italo, 2026-11-25)

## Datos e imágenes

- **free-exercise-db** (dominio público): se usan sus datos y **sus fotos**. (2026-11-23)
- **openGym**: **solo el texto** (nombres e instrucciones en español). **Sus imágenes nunca** (licencia privada de Gymvisual). (2026-11-23)
- No usar imágenes de ExerciseDB, WorkoutLabs, RepDB ni Exercise Animatic. (2026-11-23 / 2026-11-25)
- Catálogo curado propio en `data/ejercicios.json` es la fuente de verdad de músculos y equivalencias. (2026-11-23)
- Conteo semanal ponderado: **principal = 1, secundario = 0,5**. Configurable. (2026-11-23)
- Metas semanales por músculo: las define el usuario en la app (`meta_semanal: null` por defecto). (2026-11-23)

## Progresión y esfuerzo (Italo, 2026-11-24, reemplaza "todas las series al tope")

- Rango de repeticiones + **RIR 1-2 en cada serie**. Es normal que las reps bajen de serie en serie (10, 9, 8).
- Se registra **peso, reps y RIR** de cada serie.
- **Subir peso** cuando la **última serie** llega al tope del rango con RIR 1-2. Salto de **~5-8%** o el mínimo del equipo. Con el peso nuevo la última serie debería caer cerca del mínimo.
- **Sesión siguiente al salto**: RIR ≥ 3 → el salto fue chico, subir más. Bajo el mínimo → fue grande, bajar un poco.
- Descanso: **2-3 min en compuestos**, 60-90 s en aislados.
- Al iniciar un ejercicio: mostrar peso/reps/RIR de **cada serie de la sesión anterior** y la **meta de reps por serie de hoy**.
- Compuestos siempre a 1-2 RIR. Aislados a 1-2 RIR salvo la última serie, que puede ir al fallo. Explicar por qué (fallar en sentadilla cansa mucho y aporta poco). (Italo, 2026-11-23)

## Interfaz (aprobada en el prototipo)

- Celular primero: una columna de máx. 480 px, todo con el pulgar, registrar una serie en pocos toques. (2026-11-23)
- **Tema claro fijo.** El oscuro solo existe forzado con `data-theme="dark"`; no seguir el modo del sistema. (Italo, 2026-11-25)
- Pestañas: **Sesión** (entrenar; antes se llamaba "Rutina"), **Semana**, **Editar** (editor de rutina), **Esfuerzo** (guía). (2026-11-23; nombre "Sesión" por Italo, 2026-11-25)
- Todos los slots abiertos por defecto; se pliegan a mano. Mantener apretado para reordenar; advierte solo si queda antes de uno más importante. (2026-11-24)
- Encabezado fijo: título chico, cronómetro iniciar/pausar con estimado, muñeco de músculos. (2026-11-24)
- Opciones A/B/C con foto animada de 2 cuadros; solo se anima la del ejercicio en curso. kg/lb por slot. (2026-11-24 / 2026-11-25)
- Sin advertencias en las tarjetas; progresión y equivalencia van en un "Detalles" discreto. Sin mensaje cuando la serie salió bien. (2026-11-24 / 2026-11-25)
- **Sesión parte en un inicio**: la rutina que toca según la rotación (sugerida), las demás para elegir cualquiera, y botón para crear rutina; cada una se puede editar. Editar tiene chips por rutina. (Italo, 2026-11-25)
- Técnica por ejercicio con los tres puntitos de la foto; drop sets; biseries entre slots seguidos; descanso con barra y ±15 s; agregar ejercicio entre slots; deslizar para borrar serie. (2026-11-25)

## Mapa de calor muscular (Italo, 2026-11-25)

- Figura musculosa de frente y espalda, piel durazno `#F6CBA8`, contorno café `#B5714A`.
- Músculos que tocan hoy: **solo borde rojo al inicio**, sin relleno; se pintan de piel a rojo según las series hechas. Los que no tocan: piel con borde café.
- En el encabezado va sin recuadro, con el conteo de series al costado.

## Íconos de ejercicios

- Decisión: **íconos propios**. Figura plana, vista lateral, músculos principales en rojo `#E5484D` (secundarios al 45%), equipo gris oscuro, 2 cuadros inicio/fin. (2026-11-25)
- **Pendiente de Italo**: elegir entre pipeline propio (MediaPipe), íconos hechos con ChatGPT o comprar (Gymvisual si confirman por escrito que se pueden editar/usar con IA; exerciseimages.com como respaldo). Ver `BITACORA.md`.
