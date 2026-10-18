"""Cuatro planos sobre el TCL y una probabilidad de estatura.

Render: python -m manim -ql estaturas.py EstaturasChile
Los parámetros son ilustrativos: no constituyen datos medidos de Chile.
No requiere LaTeX, audio, archivos externos ni conexión al renderizar.
"""

from math import erfc, exp, isfinite, pi, sqrt

import numpy as np
from manim import (
    Axes, BLUE_C, Create, DashedLine, DOWN, FadeIn, FadeOut, GOLD,
    GREEN_C, LaggedStart, LEFT, MovingCameraScene,
    Rectangle, RIGHT, RoundedRectangle, Text,
    Transform, UP, VGroup, WHITE, Write, config,
)


# Centímetros. Sustituir con estimaciones de una fuente y población definidas.
MEDIA = 173.0
DESVIACION = 7.0
UMBRAL = 190.0
POBLACION = "Hombres adultos en Chile · ejemplo ilustrativo"
SEMILLA = 2026
FONDO = "#101827"
TENUE = "#A9B8CC"


def probabilidad_superior(umbral=UMBRAL, media=MEDIA, desviacion=DESVIACION):
    """Cola normal estable, sin restar de 1 una CDF próxima a 1."""
    if not all(isfinite(x) for x in (umbral, media, desviacion)):
        raise ValueError("Los parámetros deben ser finitos.")
    if desviacion <= 0:
        raise ValueError("La desviación estándar debe ser positiva.")
    return 0.5 * erfc((umbral - media) / (desviacion * sqrt(2)))


def decimal(valor, lugares=2):
    return f"{valor:.{lugares}f}".replace(".", ",")


def texto(contenido, tam=28, color=WHITE):
    return Text(contenido, font="DejaVu Sans", font_size=tam, color=color)


def normal(x, media=0.0, desviacion=1.0):
    return exp(-0.5 * ((x - media) / desviacion) ** 2) / (desviacion * sqrt(2 * pi))


class PlanoBase(MovingCameraScene):
    def setup(self):
        super().setup()
        self.camera.background_color = FONDO
        self.vertical = config.frame_height > config.frame_width
        # Validar también cuando se usa únicamente el plano introductorio.
        probabilidad_superior()

    def cabecera(self, numero, titulo, subtitulo):
        if self.vertical:
            titulos = {
                1: "De muchas contribuciones\na una campana",
                2: "Un modelo para\nlas estaturas",
                3: f"¿Qué tan probable es\nsuperar {UMBRAL:g} cm?",
                4: "De una cola\na una probabilidad",
            }
            etiqueta = texto(f"{numero:02d}  /  ESTATURAS", 22, BLUE_C)
            titulo_m = texto(titulos[numero], 36)
            if titulo_m.width > 7.4:
                titulo_m.scale_to_fit_width(7.4)
            if subtitulo == POBLACION:
                subtitulo = POBLACION.replace(" · ", "\n")
            else:
                subtitulo = "Una intuición matemática\nantes de hablar de estaturas"
            sub = texto(subtitulo, 24, TENUE)
            if sub.width > 7.4:
                sub.scale_to_fit_width(7.4)
            grupo = VGroup(etiqueta, titulo_m, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.23)
            grupo.move_to(LEFT * 0.25).set_y(6.3 - grupo.height / 2)
            self.play(FadeIn(grupo, shift=DOWN * 0.15))
            return
        etiqueta = texto(f"{numero:02d}  /  ESTATURAS", 18, BLUE_C).to_corner(UP + LEFT)
        titulo_m = texto(titulo, 37).next_to(etiqueta, DOWN, aligned_edge=LEFT, buff=0.2)
        sub = texto(subtitulo, 21, TENUE).next_to(titulo_m, DOWN, aligned_edge=LEFT, buff=0.16)
        grupo = VGroup(etiqueta, titulo_m, sub)
        if grupo.width > 13.1:
            grupo.scale_to_fit_width(13.1).to_corner(UP + LEFT)
        self.play(FadeIn(grupo, shift=DOWN * 0.15))

    def aviso(self, contenido="Parámetros ilustrativos · sin una fuente chilena validada"):
        if self.vertical:
            aviso = texto("Parámetros ilustrativos\nSin una fuente chilena validada", 21, TENUE)
            aviso.move_to(LEFT * 0.25 + DOWN * 5.8)
            self.add(aviso)
            return
        aviso = texto(contenido, 17, TENUE).to_edge(DOWN, buff=0.18)
        self.add(aviso)

    def limpiar(self):
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)

    def ejes_alturas(self):
        # Incluir siempre el umbral y al menos cuatro desviaciones por lado.
        minimo = 10 * np.floor(min(MEDIA - 4 * DESVIACION, UMBRAL - DESVIACION) / 10)
        maximo = 10 * np.ceil(max(MEDIA + 4 * DESVIACION, UMBRAL + DESVIACION) / 10)
        altura = normal(MEDIA, MEDIA, DESVIACION)
        ejes = Axes(
            x_range=[minimo, maximo, 10], y_range=[0, altura * 1.2, altura / 2],
            x_length=7.0 if self.vertical else 10.8,
            y_length=3.7 if self.vertical else 3.1, tips=False,
            axis_config={"color": TENUE, "include_ticks": False},
        )
        if self.vertical:
            ejes.shift(LEFT * 0.25)
        etiquetas = VGroup(*[
            texto(f"{x:g}", 22 if self.vertical else 20, TENUE).next_to(ejes.c2p(x, 0), DOWN, buff=0.15)
            for x in np.arange(minimo, maximo + 1, 10)
        ])
        unidad = texto("Estatura (cm)", 24 if self.vertical else 20, TENUE).next_to(etiquetas, DOWN, buff=0.18)
        if self.vertical:
            densidad = texto("Densidad", 21, TENUE).next_to(ejes, UP, buff=0.5).align_to(ejes, LEFT)
        else:
            densidad = texto("Densidad", 18, TENUE).next_to(ejes, LEFT, buff=0.12).rotate(pi / 2)
        curva = ejes.plot(lambda x: normal(x, MEDIA, DESVIACION), color=BLUE_C)
        return ejes, VGroup(etiquetas, unidad, densidad), curva

    def plano_tcl(self):
        self.cabecera(1, "De muchas contribuciones a una campana",
                      "Una intuición matemática antes de hablar de estaturas")
        ejes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.65, 0.2],
                    x_length=7.0 if self.vertical else 10.7,
                    y_length=3.7 if self.vertical else 3.0, tips=False,
                    axis_config={"include_ticks": False, "color": TENUE}).shift(DOWN * 0.25)
        if self.vertical:
            ejes.shift(LEFT * 0.25)
        etiquetas = VGroup(*[
            texto(str(x), 20, TENUE).next_to(ejes.c2p(x, 0), DOWN, buff=0.12)
            for x in range(-3, 4)
        ])
        ecuacion = texto("Zₙ = (X₁ + ··· + Xₙ − nμ) / (σ√n)", 28).move_to(DOWN * 2.45)
        condicion = texto("Variables i.i.d. · varianza finita y positiva", 20, TENUE).move_to(DOWN * 3.04)
        if self.vertical:
            ecuacion = texto("Zₙ = (X₁ + ··· + Xₙ − nμ)\n/ (σ√n)", 29).move_to(LEFT * 0.25 + DOWN * 3.2)
            condicion = texto("Variables independientes\ne idénticamente distribuidas\nVarianza finita y positiva", 23, TENUE).move_to(LEFT * 0.25 + DOWN * 4.65)
        self.play(Create(ejes), FadeIn(etiquetas), Write(ecuacion), FadeIn(condicion))
        referencia = ejes.plot(normal, color=GOLD, stroke_width=3)
        leyenda = texto("Referencia: normal estándar", 19, GOLD).move_to(RIGHT * 3.5 + UP * 1.35)
        if self.vertical:
            leyenda = texto("Referencia: normal estándar", 22, GOLD).move_to(LEFT * 0.25 + UP * 2.5)
        self.play(Create(referencia), FadeIn(leyenda))
        rng = np.random.default_rng(SEMILLA)
        muestras = rng.uniform(-0.5, 0.5, size=(40000, 40))
        acumuladas = muestras.cumsum(axis=1)
        bordes = np.linspace(-4, 4, 49)

        def histograma(n):
            valores = acumuladas[:, n - 1] / sqrt(n / 12)
            # Dividir por la muestra completa, sin renormalizar al rango visible.
            cuentas, _ = np.histogram(valores, bins=bordes)
            densidades = cuentas / (len(valores) * np.diff(bordes))
            barras = VGroup()
            for inicio, fin, densidad in zip(bordes[:-1], bordes[1:], densidades):
                barra = Rectangle(
                    width=(ejes.c2p(fin, 0) - ejes.c2p(inicio, 0))[0] * 0.94,
                    height=max(float(densidad) * ejes.y_axis.unit_size, 0.001),
                    stroke_width=0, fill_color=BLUE_C, fill_opacity=0.65,
                ).move_to(ejes.c2p((inicio + fin) / 2, float(densidad) / 2))
                barras.add(barra)
            return barras

        barras = histograma(1)
        contador = texto("n = 1 contribución", 24, BLUE_C).move_to(LEFT * 3.2 + UP * 1.35)
        if self.vertical:
            contador.move_to(LEFT * 0.25 + UP * 3.05)
        self.play(FadeIn(barras), FadeIn(contador))
        self.wait(1.5)
        for n in (2, 5, 15, 40):
            nuevo = texto(f"n = {n} contribuciones", 24, BLUE_C).move_to(contador)
            self.play(Transform(barras, histograma(n)), Transform(contador, nuevo), run_time=1.1)
            self.wait(1)
        self.wait(1.5)

    def plano_estaturas(self):
        self.cabecera(2, "Un modelo para las estaturas", POBLACION)
        self.aviso()
        ejes, etiquetas, curva = self.ejes_alturas()
        self.play(Create(ejes), FadeIn(etiquetas))
        self.play(Create(curva), run_time=1.5)
        marcas = VGroup()
        for x, etiqueta, color in (
            (MEDIA - DESVIACION, "μ − σ", TENUE),
            (MEDIA, "μ", GOLD),
            (MEDIA + DESVIACION, "μ + σ", TENUE),
        ):
            linea = DashedLine(ejes.c2p(x, 0), ejes.c2p(x, normal(x, MEDIA, DESVIACION)), color=color)
            rotulo = texto(etiqueta, 23, color).next_to(linea, UP, buff=0.1)
            marcas.add(VGroup(linea, rotulo))
        self.play(LaggedStart(*[FadeIn(m) for m in marcas], lag_ratio=0.35))
        parametros = texto(f"μ = {MEDIA:g} cm     σ = {DESVIACION:g} cm", 28, GOLD).move_to(DOWN * 2.65)
        detalle = texto("El TCL motiva la intuición; el ajuste requiere datos de esa población.", 20, TENUE).move_to(DOWN * 3.15)
        if self.vertical:
            parametros = texto(f"μ = {MEDIA:g} cm\nσ = {DESVIACION:g} cm", 33, GOLD).move_to(LEFT * 0.25 + DOWN * 3.5)
            detalle = texto("El TCL motiva la intuición.\nEl ajuste requiere datos\nde esa población.", 23, TENUE).move_to(LEFT * 0.25 + DOWN * 4.8)
        self.play(Write(parametros), FadeIn(detalle))
        self.wait(4)

    def plano_cola(self):
        self.cabecera(3, f"¿Cuál es la probabilidad de superar {UMBRAL:g} cm?", POBLACION)
        self.aviso()
        ejes, etiquetas, curva = self.ejes_alturas()
        self.play(Create(ejes), FadeIn(etiquetas), Create(curva))
        extremo = ejes.x_range[1]
        area = ejes.get_area(curva, x_range=(UMBRAL, extremo), color=GREEN_C, opacity=0.85)
        linea = DashedLine(ejes.c2p(UMBRAL, 0), ejes.c2p(UMBRAL, normal(MEDIA, MEDIA, DESVIACION) * 0.85), color=GREEN_C)
        umbral = texto(f"{UMBRAL:g} cm", 23, GREEN_C).next_to(linea, UP, buff=0.12)
        self.play(Create(linea), FadeIn(umbral), FadeIn(area), run_time=1.5)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.48).move_to(ejes.c2p(UMBRAL + DESVIACION * 0.45, normal(MEDIA, MEDIA, DESVIACION) * 0.16)), run_time=1.5)
        self.wait(2)
        self.play(self.camera.frame.animate.restore(), run_time=1.5)
        formula = texto(f"P(H > {UMBRAL:g}) = 1 − Φ(({UMBRAL:g} − μ) / σ)", 29).move_to(DOWN * 2.75)
        aclaracion = texto("Φ: función de distribución de la normal estándar · área total = 1", 19, TENUE).move_to(DOWN * 3.2)
        if self.vertical:
            formula = texto(f"P(H > {UMBRAL:g})\n= 1 − Φ(({UMBRAL:g} − μ) / σ)", 30).move_to(LEFT * 0.25 + DOWN * 3.5)
            aclaracion = texto("Φ: distribución acumulada\nde la normal estándar\nEl área total es 1", 23, TENUE).move_to(LEFT * 0.25 + DOWN * 4.85)
        self.play(Write(formula), FadeIn(aclaracion))
        self.wait(3)

    def plano_resultado(self):
        self.cabecera(4, "De una cola a una probabilidad", POBLACION)
        self.aviso()
        z = (UMBRAL - MEDIA) / DESVIACION
        p = probabilidad_superior()
        cuenta = texto(f"z = ({UMBRAL:g} − {MEDIA:g}) / {DESVIACION:g} ≈ {decimal(z)}", 32).move_to(UP * 0.85)
        porcentaje = texto(f"P(H > {UMBRAL:g}) ≈ {decimal(p * 100)} %", 45, GREEN_C).move_to(DOWN * 0.15)
        equivalencia = texto(f"Aproximadamente 1 de cada {round(1 / p):,} personas".replace(",", "."), 29).move_to(DOWN * 1.15) if p > 0 else texto("Cola por debajo de la precisión numérica", 26)
        marco = RoundedRectangle(width=12.0, height=3.5, corner_radius=0.2,
                                 stroke_color=BLUE_C, stroke_opacity=0.45).move_to(DOWN * 0.15)
        if self.vertical:
            cuenta = texto(f"z = ({UMBRAL:g} − {MEDIA:g}) / {DESVIACION:g}\n≈ {decimal(z)}", 29).move_to(LEFT * 0.25 + UP * 1.6)
            porcentaje = texto(f"≈ {decimal(p * 100)} %", 61, GREEN_C).move_to(LEFT * 0.25)
            encabezado = texto(f"P(H > {UMBRAL:g} cm)", 27, GREEN_C).next_to(porcentaje, UP, buff=0.2)
            porcentaje = VGroup(porcentaje, encabezado)
            equivalencia = texto(f"Aproximadamente\n1 de cada {round(1 / p):,} personas".replace(",", "."), 30).move_to(LEFT * 0.25 + DOWN * 1.6) if p > 0 else texto("Cola por debajo de\nla precisión numérica", 26).move_to(DOWN * 1.6)
            marco = RoundedRectangle(width=7.5, height=6, corner_radius=0.2,
                                     stroke_color=BLUE_C, stroke_opacity=0.45).move_to(LEFT * 0.25)
        self.play(Create(marco), Write(cuenta))
        self.play(Write(porcentaje), run_time=1.5)
        self.play(FadeIn(equivalencia, shift=UP * 0.15))
        nota = VGroup(
            texto("Resultado del modelo, no una frecuencia comprobada en Chile.", 22, GOLD),
            texto("Para estimar esa frecuencia necesitamos datos y una población definida.", 20, TENUE),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 2.65)
        if self.vertical:
            nota = VGroup(
                texto("Resultado del modelo.\nNo es una frecuencia\ncomprobada en Chile.", 25, GOLD),
                texto("Necesitamos datos y una\npoblación definida.", 23, TENUE),
            ).arrange(DOWN, buff=0.3).move_to(LEFT * 0.25 + DOWN * 4.3)
        self.play(FadeIn(nota))
        self.wait(5)


class TeoremaCentralLimite(PlanoBase):
    def construct(self):
        self.plano_tcl()


class DistribucionEstaturas(PlanoBase):
    def construct(self):
        self.plano_estaturas()


class ColaSobre190(PlanoBase):
    def construct(self):
        self.plano_cola()


class ResultadoProbabilidad(PlanoBase):
    def construct(self):
        self.plano_resultado()


class EstaturasChile(PlanoBase):
    """Película completa; los planos también pueden renderizarse por separado."""

    def construct(self):
        for indice, plano in enumerate((self.plano_tcl, self.plano_estaturas,
                                        self.plano_cola, self.plano_resultado)):
            if indice:
                self.limpiar()
            plano()
