# Contexto del proyecto: app personal de entrenamiento

> Documento original de requisitos (2026-11-23). Lo vigente está en `DECISIONES.md`; si algo choca, manda ese.

## Quién y para qué
Es una app para uso personal de Italo (un solo usuario). No es para publicar ni vender. El objetivo es reemplazar las apps de gimnasio comerciales, que le fallan por tener publicidad, funciones de pago o interfaces incómodas.

## El problema real
Italo entrena en un gimnasio lleno. Los equipos se ocupan, hay que esperar turno y tiene que decidir sobre la marcha qué ejercicio usar en vez del que quería. Esa decisión le quita tiempo, y su tiempo es limitado: entrena unos 60-70 minutos porque después tiene que sacar al perro, cocinar, etc.

Lo que más le frena el progreso no es la falta de conocimiento. Es:
1. Perder tiempo decidiendo alternativas en el momento.
2. Saltarse un día y que un músculo quede sin trabajar dos semanas seguidas.
3. No tener claro cuántas series duras lleva por músculo en la semana.

## El problema de fondo (lo que las apps no resuelven)
Casi todas las apps resuelven el problema de "no sé qué rutina hacer": te entregan una rutina. Pero al ser rutinas rígidas, crean otro problema que nadie resuelve bien: **"¿cómo reemplazo este ejercicio?"**

- La app dice "pec deck" y la máquina no existe, está rota o siempre tiene 4-5 personas esperando (caso real del gimnasio de Italo: hay una sola máquina de apertura de pecho y siempre hay fila).
- Quien tiene experiencia sabe que hay alternativas (mancuernas, polea, flexiones), pero **un principiante no sabe cuál elegir, no sabe si es equivalente, y no tiene la confianza de salirse de lo que le dijo la app**. Entonces espera la fila, se salta el ejercicio o abandona la sesión.
- Italo también lo vive: decidir la alternativa en el momento le quita tiempo, y a veces elige una que trabaja el músculo muy distinto, con lo que ese músculo queda mal estimulado esa semana.

**Meta del proyecto:** que el reemplazo de un ejercicio sea una decisión rápida, segura y explicada, no una improvisación. La app debe enseñar *por qué* una alternativa es equivalente, para que con el tiempo el usuario gane criterio propio.

## Idea central de diseño
La app se organiza por **slots con alternativas ordenadas**, y mide **series por músculo a la semana**, no ejercicios fijos.

### 1. Slots con 3 alternativas
Cada día tiene slots (por ejemplo "press pesado", "tirón vertical"). Cada slot trae 3 ejercicios ya ordenados: A, B y C.
- Si A está ocupado y no hay turno inmediato, se usa B sin pensar. C es el plan de emergencia.
- Los tres cubren el mismo músculo y patrón de movimiento, para que el estímulo sea parecido.
- La app registra **cuál alternativa se usó**, porque el progreso (peso y repeticiones) se compara contra el mismo ejercicio.

### 1b. Reemplazo guiado y explicado
- Cada ejercicio tiene un botón **"Ocupado / no disponible"** que lo cambia al instante por la mejor alternativa disponible, sin pensar.
- Cada alternativa muestra una explicación corta de por qué es equivalente. Ejemplo para pec deck: "Cruces en polea: mismo movimiento de aducción horizontal, tensión constante, ajusta el peso fácil" / "Aperturas con mancuernas: mismo patrón, más tensión al estirar, menos al cerrar" / "Flexiones con peso: no aísla igual, pero trabaja el mismo músculo si no hay nada más".
- Criterios para que dos ejercicios cuenten como equivalentes: mismo músculo principal, patrón de movimiento parecido, rango de repeticiones similar y equipo distinto.
- Cada alternativa lleva una nota de ajuste (por ejemplo "con mancuernas usa ~30-40% menos peso que en máquina", "baja el peso la primera vez y busca llegar a 1-2 repeticiones en reserva") y una nota de técnica para quien no la conoce.
- Pensado también para principiantes: lenguaje simple, sin jerga, y la confianza de que cambiar un ejercicio por su alternativa **no arruina la rutina**.

### 2. Conteo semanal de series por músculo
La app lleva las series duras de la semana por músculo contra una meta, y avisa qué músculo va atrasado.

Metas semanales aproximadas (series duras):
- Espalda: 14-16
- Pecho: 12-14
- Cuádriceps: 10-12
- Isquios y glúteos: 10-12
- Hombro lateral: 8-10
- Hombro posterior: 8-10
- Tríceps: 8-10
- Bíceps: 8-10
- Pantorrillas: 6-8

### 2b. Peso (importancia) de cada ejercicio
Las apps tratan todos los ejercicios al mismo nivel, y no es así. Un ejercicio compuesto como dominadas o sentadilla vale mucho más dentro de la rutina que uno de aislamiento como bíceps, antebrazo o gemelos, porque trabaja varios músculos a la vez.

- Cada ejercicio tiene un **músculo principal** y **músculos secundarios**, y cada uno aporta un peso distinto al conteo de series. Ejemplo: una serie de dominadas cuenta 1 para espalda y ~0,5 para bíceps; una sentadilla cuenta 1 para cuádriceps y ~0,5 para glúteos (e isquios en menor medida).
- Los pesos son configurables. Valor inicial sugerido: principal = 1, secundario = 0,5.
- Cada slot tiene una **prioridad** (alta para compuestos pesados, media para compuestos livianos, baja para aislados).
- **Cuando falta tiempo:** la app debe decir qué conviene sacrificar. Quedar corto en 3 series de bíceps pesa mucho menos que quedar corto en 3 series de dominadas, porque las dominadas ya dan estímulo indirecto a bíceps. Regla: se recorta primero lo de prioridad baja, y los compuestos se protegen.
- El conteo de series por músculo del punto siguiente usa estos pesos, no solo "una serie = una serie".

### 2c. Orden de los ejercicios y fatiga
El orden dentro de la sesión cambia el rendimiento. Quien parte con jalón al pecho y después hace remo rinde menos en el remo que el día que partió con remo, porque ya llega cansado. Las apps no reflejan esto y por eso el progreso parece estancarse o retroceder sin que sea cierto.

- Cada registro guarda **la posición del ejercicio en la sesión** (1º, 2º, 3º...), además del peso y las repeticiones.
- La comparación con la sesión anterior debe considerar la posición: comparar "remo como 1er ejercicio" contra "remo como 1er ejercicio", y marcar cuando el orden cambió para no interpretar una baja de rendimiento como pérdida de fuerza.
- Aviso tipo: "La última vez hiciste este ejercicio de 1º, hoy va de 3º, es normal que rindas algo menos".
- El orden recomendado por defecto es: compuestos pesados primero, aislados al final, y el músculo más atrasado de la semana al principio.
- Si el usuario cambia el orden (porque una máquina estaba ocupada), la app lo registra y ajusta la expectativa de peso y repeticiones.

### 2d. Reordenar la sesión cuando hay espera
A veces ninguna de las alternativas A/B/C del slot está disponible. En vez de esperar parado, la app sugiere **mover el ejercicio y rellenar el tiempo con otro que no interfiera**.

- **Sugerencia de reordenamiento:** si el slot actual está bloqueado, la app propone hacer mientras tanto otro ejercicio del día que no use los músculos del ejercicio principal que viene. Ejemplo: se espera una máquina de press de pecho, así que mientras tanto se hacen elevaciones laterales (trabajan hombro lateral y no cansan el pecho ni el tríceps que se necesitan para el press). Cuando la máquina se desocupa, se vuelve al ejercicio principal.
- **Criterio para sugerir:** el ejercicio de relleno no debe compartir músculo principal ni secundario relevante con el ejercicio principal que viene después, y debe ser de fatiga baja (aislados, como laterales, curl, pantorrillas, abdomen, face pull).
- **Reordenamiento manual con advertencia:** si el usuario mueve un ejercicio a mano y lo pone antes de un compuesto que comparte músculos con él, la app muestra una advertencia, por ejemplo: "Este ejercicio fatiga el mismo músculo que usarás en tu ejercicio principal. Es posible que rindas menos y no notes el progreso que esperas".
- La advertencia es informativa, no bloquea: el usuario decide. Si igual lo hace, el registro queda marcado con la posición y la advertencia, para que la comparación con la sesión anterior (punto 2c) la tenga en cuenta.
- Esto se apoya en el mapa de músculos principales y secundarios de cada ejercicio (punto 2b): sirve tanto para ponderar series como para decidir qué ejercicios interfieren entre sí.

### 3. Día 4 de rescate
Hay 4 días: pecho/hombro/tríceps, espalda/bíceps, pierna y un cuarto día flexible.
- El día 4 **completa lo que faltó** en la semana, empezando por el músculo más atrasado según el conteo.
- Si no falta nada, hace una segunda dosis liviana de tren superior (1 press, 1 remo, 1 lateral, 1 de brazos, 2-3 series cada uno).
- Objetivo: nunca pasen dos semanas sin trabajar un músculo por haberse saltado un día.

### 4. Cero decisiones en el gimnasio
La pantalla principal debe mostrar el slot actual, las alternativas A/B/C, el peso y repeticiones de la última vez, y un botón rápido para registrar la serie. Debe ser usable con una mano, entre series, en el celular.

## Rutina base
La rutina personal de Italo quedó fuera del repo a pedido suyo: la app parte en blanco y cada usuario arma sus slots en la pestaña Editar. La estructura de 4 días (empuje, tirón, pierna, día 4 de rescate) se mantiene como idea de diseño.

## Reglas de intensidad y progresión
- Compuestos (slots 1-3): dejar 1-2 repeticiones en reserva, sin llegar al fallo.
- Aislados: la última serie puede ir al fallo o a 1 en reserva.
- Descanso: 2-3 min en compuestos, 60-90 s en aislados.
- Progresión: **reemplazada el 2026-11-24**. La regla vigente está en `DECISIONES.md` (sube peso cuando la última serie llega al tope con RIR 1-2).
- Semana liviana cada 5-6 semanas.
- Si en una serie no se llega a las repeticiones objetivo, es válido hacer una serie descendente (bajar peso y sumar repeticiones), pero lo preferible es descansar más entre series.

## Requisitos técnicos
- **Web app personal** que se abre en el navegador del celular y se guarda como ícono en la pantalla de inicio (PWA). No se publica en tiendas de apps. Sin publicidad ni pagos.
- **Datos en Google Sheets** en su Drive (por ejemplo vía Google Apps Script o la API de Sheets), para tener siempre una planilla visible y editable como respaldo.
- **Base de ejercicios abierta**, para no crearlos a mano. Opciones a evaluar:
  - free-exercise-db (GitHub, ~800 ejercicios con músculo, equipo e instrucciones, gratis)
  - wger (API abierta y app de código abierto)
  - ExerciseDB (API gratuita con animaciones)
- Repo en GitHub.
- Italo sabe Python. Conviene mantener el stack simple y fácil de modificar por él.

## Funciones mínimas (primera versión)
1. Plantilla de rutina con slots y alternativas A/B/C, editable.
2. Botón "Ocupado / no disponible" que cambia el ejercicio por su alternativa, con la explicación de por qué es equivalente y cómo ajustar el peso.
2b. Registro de series: ejercicio usado, peso, repeticiones, esfuerzo (repeticiones en reserva).
3. Mostrar el último registro del mismo ejercicio al iniciar un slot, indicando en qué posición de la sesión se hizo esa vez.
4. Conteo semanal de series por músculo contra metas, ponderado (principal = 1, secundario = 0,5), con aviso del músculo más atrasado.
4b. Prioridad por ejercicio, para saber qué recortar cuando falta tiempo.
4c. Reordenamiento: sugerir un ejercicio de relleno que no interfiera mientras se espera una máquina, y advertir cuando un reordenamiento manual fatiga los músculos del ejercicio principal.
5. Sugerencia del día 4 según lo que falta.
6. Guardado en Google Sheets.

## Ideas para después
- Aviso cuando se cumple el tope de repeticiones en todas las series y toca subir peso.
- Gráfico de progresión por ejercicio y por músculo.
- Temporizador de descanso.
- Peso corporal y % de grasa (Italo mide con una balanza Fitdays).

## Instrucción para el asistente de código
El stack ya está decidido (ver `README.md`). Prioriza que funcione bien en el celular y que registrar una serie tome muy pocos toques.
