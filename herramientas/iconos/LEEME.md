# Generador de íconos (prototipo)

Experimento para crear íconos propios de ejercicios a partir de las fotos de dominio público de free-exercise-db.

1. `pose.py`: corre MediaPipe Pose Landmarker sobre las fotos (`../fotos/*.jpg`) y guarda los puntos 3D en `poses.json`. Necesita `pip install mediapipe` y el modelo `pose_heavy.task` (se descarga de Google, no está en el repo).
2. `render.py`: convierte esos puntos en ángulos articulares y dibuja una figura plana SVG de vista lateral con proporciones fijas, músculos en rojo y equipo en gris. Genera 2 cuadros (inicio/fin) por ejercicio.

Limitación conocida: MediaPipe falla en poses acostadas (press banca) y con brazos tras la nuca (sentadilla); `render.py` corrige esos casos con reglas por ejercicio (`static`, `arms`, `lying`).

Muestra del resultado: `docs/img/iconos-muestra.png`. Las fotos de entrada y las salidas no se versionan.
