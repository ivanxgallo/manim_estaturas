# Estaturas: una historia con Manim

Animación en español con cuatro planos: teorema central del límite, modelo
normal de estaturas, cola sobre 190 cm y cálculo de su probabilidad.
Incluye una película completa y cuatro escenas independientes. Sin audio;
los textos en pantalla sirven de guía para una futura narración.

[Video vertical exportado con LaTeX (1080 × 1920)](ejemplos/EstaturasChileVertical.mp4).

## Jupyter / Google Colab

Abre [`estaturas_jupyter.ipynb`](estaturas_jupyter.ipynb) y ejecuta las celdas
en orden. El notebook incluye todo el código, prepara dependencias, renderiza
y muestra el MP4 dentro de Jupyter. No requiere clonar el repositorio.
En Google Colab incluye una celda para descargar el video.

Usa Python 3.11 o posterior. La configuración inicial es vertical 9:16 en
vista previa; cambia `CALIDAD` a `"final"` para exportar 1080 × 1920 a 30 fps.
También puedes elegir formato horizontal. En Jupyter local, Cairo/Pango y
LaTeX requieren instalación del sistema; la primera celda explica los permisos y
comandos necesarios. No se ha validado en Windows nativo: usa WSL/Ubuntu.

Los cambios en `estaturas.py` no actualizan automáticamente la copia incluida
en el notebook; ambas versiones contienen las mismas escenas en esta entrega.

## Instalación

Requiere Python 3.11 o posterior y las bibliotecas de desarrollo Cairo/Pango.
En Debian/Ubuntu, con permisos de administración:

```bash
sudo apt-get update
sudo apt-get install -y build-essential pkg-config libcairo2-dev libpango1.0-dev ffmpeg texlive-latex-base texlive-latex-extra texlive-fonts-recommended lmodern dvisvgm
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Las ecuaciones usan **`MathTex`**: fracciones, raíces, subíndices y símbolos
se compilan con LaTeX. Los títulos y explicaciones usan **`Tex`** con
**Latin Modern**, la versión vectorial de Computer Modern. Ambos comparten
plantilla y familia tipográfica. `pip install manim` no instala TeX Live.

Comprueba `latex --version`, `dvisvgm --version` y
`kpsewhich lmodern.sty` antes de renderizar. El notebook comprueba estas
dependencias incluso si Manim ya estaba instalado.

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
Por indicación del usuario, el ejemplo usa **172 cm**, **7 cm** y **190 cm**.
La encuesta, el período y el rango de edad de esos parámetros están pendientes
de identificar. No se atribuyen a ENS 2016-2017. La comparación con una copia
pública de los microdatos ENS y el cálculo reproducible se documentan en
[`FUENTES.md`](FUENTES.md) y [`analizar_ens.py`](analizar_ens.py).
El usuario explicará las estimaciones en su narración; la animación no muestra
advertencias sobre ellas en pantalla.

El **teorema central del límite (TCL)** se ilustra con 40.000 simulaciones reproducibles de sumas de variables
uniformes independientes e idénticamente distribuidas. Cada suma se centra y
escala por su desviación estándar. Esto ilustra un teorema; no demuestra la
normalidad de las estaturas ni estima parámetros chilenos.

La cola se calcula como `0.5 * erfc(z / sqrt(2))`, sin integrar el dibujo
truncado. Con los parámetros actuales da aproximadamente **0,506 %**, o
**1 de cada 197**. La equivalencia representa una frecuencia esperada bajo el
modelo, no una garantía para un grupo concreto de personas.
