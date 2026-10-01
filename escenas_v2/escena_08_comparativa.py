"""
escenas_v2/escena_08_comparativa.py
Escena 8: Comparativa visual estructurada y didáctica.
Terminología homogénea: O(1) promedio, sin textos solapados.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_NODO = BLUE_C
C_APAGADO = GRAY_B
C_ENTRADA = TEAL


class Escena08Comparativa(Scene):
    def cuadro(self, txt, x, y, w=0.72, h=0.54, size=20, color=GRAY_B):
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.2)
        return VGroup(r, Text(str(txt), font_size=size)).move_to([x, y, 0])

    def crear_tarjeta_estado(self, texto, x, y, color):
        caja = RoundedRectangle(
            corner_radius=0.1, width=5.6, height=0.62,
            stroke_color=color, stroke_width=2,
            fill_color="#081c1c" if color == C_OK else "#241010",
            fill_opacity=0.9
        ).move_to([x, y, 0])
        t = Text(texto, font_size=16, color=color, weight=BOLD).move_to(caja)
        return VGroup(caja, t)

    def texto_inf(self, txt, color=WHITE, y=-3.15, size=21):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO Y LÍNEA DIVISORIA CENTRAL (0:00 - 0:05)
        # -------------------------------------------------------------
        titulo = Text("Búsqueda y Reordenamiento: get(8)", font_size=38, color=YELLOW)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)

        divisoria = Line([0, 2.4, 0], [0, -2.7, 0], color=GRAY, stroke_width=2)
        h_izq = Text("Enfoque Ingenuo (Arreglo)", font_size=21, color=C_MAL, weight=BOLD).move_to([-3.6, 2.3, 0])
        h_der = Text("LRU Cache (Hash + Lista)", font_size=21, color=C_OK, weight=BOLD).move_to([3.6, 2.3, 0])
        self.play(Create(divisoria), FadeIn(h_izq), FadeIn(h_der), run_time=0.7)
        self.wait(1.5)

        # -------------------------------------------------------------
        # 2. LADO IZQUIERDO: ARREGLO (Búsqueda N + Desplazamiento N) (0:05 - 0:14)
        # -------------------------------------------------------------
        claves = [5, 2, 9, 4, 7, 1, 8]
        y_arr = 1.05
        celdas = [self.cuadro(k, -5.9 + i * 0.74, y_arr) for i, k in enumerate(claves)]
        grupo_celdas = VGroup(*celdas)
        self.play(FadeIn(grupo_celdas), run_time=0.6)

        cursor = Triangle(color=C_ACTIVO, fill_opacity=1).scale(0.13).move_to([-5.9, y_arr - 0.48, 0])
        tarjeta_izq = self.crear_tarjeta_estado("Paso 1: Búsqueda lineal (recorre casillas)", -3.6, -1.45, C_MAL)
        self.play(FadeIn(cursor), FadeIn(tarjeta_izq), run_time=0.5)

        for i in range(len(claves)):
            if i > 0:
                self.play(cursor.animate.move_to([-5.9 + i * 0.74, y_arr - 0.48, 0]), run_time=0.22)
            es_obj = (claves[i] == 8)
            self.play(celdas[i][0].animate.set_stroke(C_OK if es_obj else C_ACTIVO, width=4), run_time=0.12)

        self.wait(0.6)
        # Desvanecemos el cursor para no dejar flechas huérfanas
        self.play(FadeOut(cursor), run_time=0.3)

        tarjeta_izq_p2 = self.crear_tarjeta_estado("Paso 2: Desplaza N elementos para reordenar", -3.6, -1.45, C_MAL)
        self.play(Transform(tarjeta_izq, tarjeta_izq_p2), run_time=0.5)

        c8 = celdas[-1]
        self.play(c8.animate.shift(UP * 0.6), run_time=0.4)
        self.play(*[celdas[j].animate.shift(RIGHT * 0.74) for j in range(len(claves) - 1)], run_time=0.6)
        self.play(c8.animate.move_to([-5.9, y_arr, 0]), run_time=0.4)

        resumen_izq = Text("Costo Total: O(N) lineal", font_size=18, color=C_MAL, weight=BOLD).move_to([-3.6, -2.25, 0])
        self.play(FadeIn(resumen_izq), run_time=0.5)
        self.wait(1.8)

        # -------------------------------------------------------------
        # 3. LADO DERECHO: LRU CACHE (Hash O(1) + Punteros O(1)) (0:14 - 0:24)
        # -------------------------------------------------------------
        m = 7
        y_bkt = 1.3
        buckets = [self.cuadro("", 1.4 + i * 0.72, y_bkt, w=0.66, h=0.42) for i in range(m)]
        indices = [Text(str(i), font_size=12, color=C_APAGADO).move_to([1.4 + i * 0.72, y_bkt + 0.35, 0]) for i in range(m)]
        grupo_hash = VGroup(*buckets, *indices)

        y_lst = -0.25
        n_c3 = RoundedRectangle(corner_radius=0.08, width=1.35, height=0.65, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=0.9).move_to([2.0, y_lst, 0])
        t_c3 = Text("K: 3", font_size=16, color=WHITE).move_to(n_c3)
        g_3 = VGroup(n_c3, t_c3)

        n_c2 = RoundedRectangle(corner_radius=0.08, width=1.35, height=0.65, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=0.9).move_to([3.6, y_lst, 0])
        t_c2 = Text("K: 2", font_size=16, color=WHITE).move_to(n_c2)
        g_2 = VGroup(n_c2, t_c2)

        n_c8 = RoundedRectangle(corner_radius=0.08, width=1.35, height=0.65, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=0.9).move_to([5.2, y_lst, 0])
        t_c8 = Text("K: 8", font_size=16, color=YELLOW, weight=BOLD).move_to(n_c8)
        g_8 = VGroup(n_c8, t_c8)

        lbl_head = Text("Head (MRU)", font_size=13, color=C_OK).next_to(g_3, DOWN, buff=0.15)

        fl_32 = DoubleArrow(g_3.get_right(), g_2.get_left(), buff=0.06, stroke_width=2.5, color=GRAY_B, tip_length=0.14)
        fl_28 = DoubleArrow(g_2.get_right(), g_8.get_left(), buff=0.06, stroke_width=2.5, color=GRAY_B, tip_length=0.14)
        g_lista = VGroup(g_3, g_2, g_8, fl_32, fl_28, lbl_head)

        self.play(FadeIn(grupo_hash), FadeIn(g_lista), run_time=0.7)
        self.wait(0.5)

        # Paso 1: Hash directo
        tarjeta_der = self.crear_tarjeta_estado("Paso 1: Hash accede en O(1) promedio", 3.6, -1.45, C_OK)
        self.play(FadeIn(tarjeta_der), run_time=0.4)

        formula = Text("8 % 7 = 1", font_size=15, color=C_ACTIVO, weight=BOLD).move_to([2.12, 0.6, 0])
        salto = Arrow(buckets[1].get_bottom(), g_8.get_top(), buff=0.08, color=C_ENTRADA, stroke_width=3, tip_length=0.15)
        self.play(FadeIn(formula), buckets[1][0].animate.set_stroke(C_ACTIVO, width=4), run_time=0.5)
        self.play(GrowArrow(salto), g_8[0].animate.set_stroke(C_OK, width=4), run_time=0.5)
        self.wait(0.7)

        # Paso 2: move_to_front (texto pedagógico y sin contradicciones)
        tarjeta_der_p2 = self.crear_tarjeta_estado("Paso 2: Reenlaza a Head con punteros O(1)", 3.6, -1.45, C_OK)
        self.play(Transform(tarjeta_der, tarjeta_der_p2), run_time=0.5)

        self.play(FadeOut(salto), FadeOut(fl_32), FadeOut(fl_28), run_time=0.35)
        self.play(g_8.animate.shift(UP * 0.65), run_time=0.45)
        self.play(
            g_3.animate.move_to([3.6, y_lst, 0]),
            g_2.animate.move_to([5.2, y_lst, 0]),
            lbl_head.animate.move_to([2.0, y_lst - 0.48, 0]),
            run_time=0.6
        )
        self.play(g_8.animate.move_to([2.0, y_lst, 0]), run_time=0.45)

        fl_83 = DoubleArrow(g_8.get_right(), g_3.get_left(), buff=0.06, stroke_width=2.5, color=C_OK, tip_length=0.14)
        fl_32_n = DoubleArrow(g_3.get_right(), g_2.get_left(), buff=0.06, stroke_width=2.5, color=C_OK, tip_length=0.14)
        self.play(Create(fl_83), Create(fl_32_n), run_time=0.5)

        # Resumen global unificado
        resumen_der = Text("Costo Global: O(1) promedio", font_size=18, color=C_OK, weight=BOLD).move_to([3.6, -2.25, 0])
        self.play(FadeIn(resumen_der), run_time=0.5)
        self.wait(1.5)

        # -------------------------------------------------------------
        # 4. REMATE PEDAGÓGICO INFERIOR (Subido a y = -3.15)
        # -------------------------------------------------------------
        pie = self.texto_inf("La LRU Cache no solo busca rápido: reordena y desaloja en O(1) promedio.", C_ACTIVO, y=-3.15)
        self.play(FadeIn(pie, shift=UP * 0.2), run_time=0.6)
        self.wait(4.0)