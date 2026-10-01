"""
escenas_v2/escena_03_una_sola_estructura.py
Escena 3: ¿Por qué no una sola estructura? (Dilema de complejidad).
Duración calibrada: ~25 segundos.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_APAGADO = GRAY_B


class Escena03UnaSolaEstructura(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO PRINCIPAL
        # -------------------------------------------------------------
        titulo = Text("¿Por qué no usar una sola estructura?", font_size=40, color=YELLOW)
        titulo.to_edge(UP, buff=0.45)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.5)

        # -------------------------------------------------------------
        # 2. ENCABEZADOS Y LÍNEA DIVISORIA (Subidos para ganar espacio)
        # -------------------------------------------------------------
        x_col1 = -6.0   # Borde izquierdo alineado dentro del encuadre
        x_col2 = 1.4    # Columna "Buscar dato"
        x_col3 = 5.0    # Columna "Reordenar por uso"

        def celda_izq(txt, y, color=WHITE, size=22):
            t = Text(txt, font_size=size, color=color)
            return t.move_to([x_col1 + t.width / 2, y, 0])

        def celda_cen(txt, x, y, color=WHITE, size=22):
            return Text(txt, font_size=size, color=color).move_to([x, y, 0])

        y_cab = 2.1
        cab = VGroup(
            celda_izq("Estructura", y_cab, C_APAGADO, 21),
            celda_cen("Buscar dato", x_col2, y_cab, C_APAGADO, 21),
            celda_cen("Reordenar por uso", x_col3, y_cab, C_APAGADO, 21)
        )
        linea_div = Line([-6.2, 1.75, 0], [6.2, 1.75, 0], color=GRAY, stroke_width=2)
        self.play(FadeIn(cab), Create(linea_div), run_time=0.7)

        # -------------------------------------------------------------
        # 3. FILAS DE LA TABLA (Distribución vertical equilibrada)
        # -------------------------------------------------------------
        filas_datos = [
            ("Arreglo / Vector", ("O(N)", C_MAL), ("O(N)", C_MAL)),
            ("Lista doblemente enlazada sola", ("O(N)", C_MAL), ("O(1)*", C_OK)),
            ("Tabla hash sola", ("O(1) promedio", C_OK), ("No guarda orden", C_MAL)),
            ("Tabla hash + Lista (LRU Cache)", ("O(1) promedio", C_OK), ("O(1)", C_OK)),
        ]

        # Fila 1: Arreglo
        y1 = 1.15
        f1 = VGroup(
            celda_izq(filas_datos[0][0], y1),
            celda_cen(filas_datos[0][1][0], x_col2, y1, filas_datos[0][1][1]),
            celda_cen(filas_datos[0][2][0], x_col3, y1, filas_datos[0][2][1])
        )
        self.play(FadeIn(f1, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(2.2)

        # Fila 2: Lista doble sola
        y2 = 0.40
        f2 = VGroup(
            celda_izq(filas_datos[1][0], y2),
            celda_cen(filas_datos[1][1][0], x_col2, y2, filas_datos[1][1][1]),
            celda_cen(filas_datos[1][2][0], x_col3, y2, filas_datos[1][2][1])
        )
        self.play(FadeIn(f2, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(2.5)

        # Fila 3: Tabla hash sola
        y3 = -0.35
        f3 = VGroup(
            celda_izq(filas_datos[2][0], y3),
            celda_cen(filas_datos[2][1][0], x_col2, y3, filas_datos[2][1][1]),
            celda_cen(filas_datos[2][2][0], x_col3, y3, filas_datos[2][2][1])
        )
        self.play(FadeIn(f3, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(3.0)

        # Fila 4: Arquitectura híbrida (Hash + Lista)
        y4 = -1.10
        f4 = VGroup(
            celda_izq(filas_datos[3][0], y4, color=YELLOW, size=23),
            celda_cen(filas_datos[3][1][0], x_col2, y4, C_OK, size=23),
            celda_cen(filas_datos[3][2][0], x_col3, y4, C_OK, size=23)
        )

        # Marco cerrado y ajustado milimétricamente dentro de la pantalla
        caja_f4 = RoundedRectangle(
            corner_radius=0.15,
            width=12.4,
            height=0.75,
            stroke_color=C_OK,
            stroke_width=3,
            fill_color="#0e2a22",
            fill_opacity=0.35
        ).move_to([0, y4, 0])

        self.play(FadeIn(f4, shift=RIGHT * 0.3), Create(caja_f4), run_time=0.8)

        # -------------------------------------------------------------
        # 4. TEXTOS DE PIE Y ACLARACIÓN (Separados para evitar solape)
        # -------------------------------------------------------------
        nota_asterisco = Text("* Solo si ya se cuenta con el puntero directo al nodo en memoria",
                              font_size=17, color=C_APAGADO).move_to([0, -2.4, 0])

        pie = Text("Se requiere acceso O(1) y reordenamiento O(1): la unión hace la fuerza.",
                   font_size=20, color=C_ACTIVO).move_to([0, -3.2, 0])

        self.play(FadeIn(nota_asterisco), FadeIn(pie, shift=UP * 0.2), run_time=0.7)
        self.wait(4.0)