"""
escenas_v2/escena_02_lru_mru.py
Escena 2: Concepto de LRU y MRU (Política de desalojo).
Duración calibrada: ~25 segundos.
"""

from manim import *

# Paleta visual consistente con el proyecto
C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_APAGADO = GRAY_B
C_FONDO_CARTA = "#0f2a33"


class Escena02LRUMRU(Scene):
    def construir_carta(self, letra, color):
        rect = RoundedRectangle(
            corner_radius=0.15,
            width=2.2,
            height=1.2,
            stroke_color=color,
            stroke_width=3.5,
            fill_color=C_FONDO_CARTA,
            fill_opacity=1
        )
        txt = Text(letra, font_size=42, color=color, weight=BOLD)
        txt.move_to(rect)
        return VGroup(rect, txt)

    def texto_inf(self, txt, color=WHITE, y=-3.3, size=22):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.8:
            t.scale_to_fit_width(12.8)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO PRINCIPAL
        # -------------------------------------------------------------
        titulo = Text("Política de desalojo: LRU", font_size=42, color=YELLOW)
        titulo.to_edge(UP, buff=0.45)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.5)

        # -------------------------------------------------------------
        # 2. CASILLEROS DE CAPACIDAD FIJA (N = 3)
        # -------------------------------------------------------------
        xs = [-3.2, 0.0, 3.2]
        y_pos = 0.3

        ranuras = VGroup(*[
            Rectangle(width=2.5, height=1.5, stroke_color=GRAY, stroke_width=2)
            .move_to([x, y_pos, 0])
            for x in xs
        ])

        lbl_mru = VGroup(
            Text("MRU (Head)", font_size=22, color=C_OK, weight=BOLD),
            Text("Más reciente", font_size=16, color=C_APAGADO)
        ).arrange(DOWN, buff=0.08).next_to(ranuras[0], UP, buff=0.35)

        lbl_lru = VGroup(
            Text("LRU (Tail)", font_size=22, color=C_MAL, weight=BOLD),
            Text("Candidato a expulsión", font_size=16, color=C_MAL)
        ).arrange(DOWN, buff=0.08).next_to(ranuras[2], UP, buff=0.35)

        self.play(FadeIn(ranuras), run_time=0.6)
        self.play(FadeIn(lbl_mru, shift=DOWN * 0.2), FadeIn(lbl_lru, shift=DOWN * 0.2), run_time=0.8)

        # Cargar cartas A, B y C
        A = self.construir_carta("A", BLUE_C).move_to([xs[0], y_pos, 0])
        B = self.construir_carta("B", TEAL).move_to([xs[1], y_pos, 0])
        C = self.construir_carta("C", PURPLE_B).move_to([xs[2], y_pos, 0])

        self.play(
            LaggedStart(
                FadeIn(A, shift=DOWN * 0.4),
                FadeIn(B, shift=DOWN * 0.4),
                FadeIn(C, shift=DOWN * 0.4),
                lag_ratio=0.3
            ),
            run_time=1.3
        )

        pie = self.texto_inf("Head = Dato más reciente  |  Tail = Dato más antiguo (menos usado)")
        self.play(FadeIn(pie), run_time=0.6)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 3. ACCESO / CONSULTA A 'C' -> PASA AL FRENTE (MRU)
        # -------------------------------------------------------------
        pie_c = self.texto_inf("Se consulta C: adquiere máxima prioridad temporal y viaja a Head (MRU)", C_ACTIVO)
        self.play(
            Transform(pie, pie_c),
            Circumscribe(C, color=C_ACTIVO, time_width=0.8),
            run_time=0.8
        )

        # C sube y viaja al frente mientras A y B se desplazan a la derecha
        self.play(C.animate.shift(UP * 1.3), run_time=0.5)
        self.play(
            C.animate.move_to([xs[0], y_pos + 1.3, 0]),
            A.animate.move_to([xs[1], y_pos, 0]),
            B.animate.move_to([xs[2], y_pos, 0]),
            run_time=1.1
        )
        self.play(C.animate.move_to([xs[0], y_pos, 0]), run_time=0.4)
        self.wait(2.5)

        # -------------------------------------------------------------
        # 4. INSERCIÓN CON CAPACIDAD LLENA: ENTRA D Y DESALOJA A B
        # -------------------------------------------------------------
        pie_d = self.texto_inf("Caché llena: entra D por Head y se expulsa el elemento en Tail (B)", C_MAL)
        D = self.construir_carta("D", ORANGE).move_to([-6.0, y_pos, 0])

        self.play(Transform(pie, pie_d), FadeIn(D, shift=RIGHT * 0.4), run_time=0.7)
        # B parpadea en rojo por ser el LRU
        self.play(B[0].animate.set_stroke(C_MAL, width=7), run_time=0.5)
        self.wait(0.4)

        # Expulsión de B hacia la derecha y avance de D, C, A
        self.play(FadeOut(B, shift=RIGHT * 1.6), run_time=0.8)
        self.play(
            D.animate.move_to([xs[0], y_pos, 0]),
            C.animate.move_to([xs[1], y_pos, 0]),
            A.animate.move_to([xs[2], y_pos, 0]),
            run_time=1.2
        )
        self.wait(1.5)

        # -------------------------------------------------------------
        # 5. CONCLUSIÓN DEL CONCEPTO
        # -------------------------------------------------------------
        pie_fin = self.texto_inf("LRU descarta siempre lo que lleva más tiempo sin utilizarse.", C_OK, size=24)
        self.play(Transform(pie, pie_fin), run_time=0.6)
        self.wait(3.5)