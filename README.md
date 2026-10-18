# Estaturas: una historia con Manim

Animación en español con cuatro planos: teorema central del límite, modelo
normal de estaturas, cola sobre 190 cm y cálculo de su probabilidad.
Incluye una película completa y cuatro escenas independientes. Sin audio;
los textos en pantalla sirven de guía para una futura narración.

## Instalación

Requiere Python 3.11 o posterior y las bibliotecas de desarrollo Cairo/Pango.
En Debian/Ubuntu, con permisos de administración:

```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libcairo2-dev libpango1.0-dev ffmpeg fonts-dejavu-core
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

No se necesita LaTeX: las fórmulas y etiquetas usan texto Unicode.

## Renderizado

Desde la raíz del repositorio:

```bash
# Vista previa: 480p, 15 fps. No abre un reproductor en el servidor.
.venv/bin/python -m manim -ql estaturas.py EstaturasChile

# Versión final: 1080p, 60 fps.
.venv/bin/python -m manim -qh estaturas.py EstaturasChile

# Un plano independiente:
.venv/bin/python -m manim -ql estaturas.py ColaSobre190
```

Los videos se guardan en `media/videos/estaturas/`, según la calidad seleccionada.
Las otras escenas son `TeoremaCentralLimite`, `DistribucionEstaturas` y
`ResultadoProbabilidad`.

## TikTok / Instagram Reels (9:16)

La composición vertical reorganiza títulos, fórmulas, leyendas y resultados,
con márgenes arriba, abajo y a la derecha para la interfaz del teléfono.
No recorta el video horizontal. Mantiene las cuatro escenas y su duración.

```bash
# Exportación vertical: 1080 × 1920, 30 fps.
.venv/bin/python -m manim --config_file manim_vertical.cfg estaturas.py EstaturasChile -o EstaturasChileVertical

# Vista previa vertical rápida: 360 × 640, 15 fps.
.venv/bin/python -m manim --config_file manim_vertical.cfg -r 360,640 --fps 15 estaturas.py EstaturasChile -o EstaturasChileVerticalPreview
```

La exportación se guarda en
`media/vertical/videos/estaturas/1920p30/EstaturasChileVertical.mp4`.
La versión horizontal sigue disponible con los comandos anteriores.

## Parámetros y rigor estadístico

Editar `MEDIA`, `DESVIACION`, `UMBRAL` (en centímetros) y `POBLACION` en
`estaturas.py`. La curva, el sombreado y los resultados comparten esos valores.
El ejemplo usa **173 cm**, **7 cm** y **190 cm**: no son estimaciones verificadas
de la población chilena. Antes de presentar el video como información empírica,
incorporar una fuente, período, población y un análisis de la adecuación del
modelo normal. La mezcla de poblaciones puede no ajustarse bien a una normal.

El TCL se ilustra con 40.000 simulaciones reproducibles de sumas de variables
uniformes independientes e idénticamente distribuidas. Cada suma se centra y
escala por su desviación estándar. Esto ilustra un teorema; no demuestra la
normalidad de las estaturas ni estima parámetros chilenos.

La cola se calcula como `0.5 * erfc(z / sqrt(2))`, sin integrar el dibujo
truncado. Con los parámetros iniciales da aproximadamente **0,758 %**, o
**1 de cada 132**. La equivalencia representa una frecuencia esperada bajo el
modelo, no una garantía para un grupo concreto de personas.
