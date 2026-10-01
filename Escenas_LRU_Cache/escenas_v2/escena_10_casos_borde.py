"""
escenas_v2/escena_10_casos_borde.py
Escena 10: Casos Borde y Robustez de Memoria en C++.
Duración calibrada: ~37 segundos.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_NODO = BLUE_C
C_APAGADO = GRAY_B
C_PANEL = "#0d1b2a"


class Escena10CasosBorde(Scene):
    def crear_tarjeta_caso(self, titulo, ancho=3.8, alto=4.2):
        marco = RoundedRectangle(
            corner_radius=0.12, width=ancho, height=alto,
            stroke_color=GRAY_B, stroke_width=2,
            fill_color=C_PANEL, fill_opacity=0.9
        )
        t_tit = Text(titulo, font_size=16, color=YELLOW, weight=BOLD).next_to(marco.get_top(), DOWN, buff=0.22)
        sep = Line(marco.get_left() + RIGHT * 0.2, marco.get_right() + LEFT * 0.2, color=GRAY, stroke_width=1.5).next_to(t_tit, DOWN, buff=0.15)
        return VGroup(marco, t_tit, sep)

    def texto_inf(self, txt, color=WHITE, y=-3.35, size=21):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO PRINCIPAL (0:00 - 0:08)
        # -------------------------------------------------------------
        titulo = Text("Casos Borde y Robustez de Memoria", font_size=36, color=YELLOW)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)

        # 3 Contenedores simétricos
        xs = [-4.1, 0, 4.1]
        c1 = self.crear_tarjeta_caso("1. Caché Vacía").move_to([xs[0], -0.25, 0])
        c2 = self.crear_tarjeta_caso("2. Un Solo Elemento").move_to([xs[1], -0.25, 0])
        c3 = self.crear_tarjeta_caso("3. Actualización de Clave").move_to([xs[2], -0.25, 0])

        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=0.8)

        pie = self.texto_inf("Validación de punteros y preservación de invariantes en situaciones límite.")
        self.play(FadeIn(pie), run_time=0.5)
        self.wait(2.0)

        # -------------------------------------------------------------
        # 2. CASO 1: CACHÉ VACÍA (0:08 - 0:17)
        # -------------------------------------------------------------
        txt_c1_op = Text("get(5) -> key not found", font_size=14, color=WHITE).move_to([xs[0], 0.8, 0])
        box_null = Rectangle(width=2.6, height=0.7, stroke_color=C_MAL, stroke_width=2, stroke_opacity=0.6).move_to([xs[0], 0.0, 0])
        lbl_null = Text("head = tail = nullptr", font_size=13, color=C_MAL).move_to(box_null)
        
        tag_res1 = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.55, stroke_color=C_OK, fill_color="#0a2618", fill_opacity=1).move_to([xs[0], -1.2, 0])
        lbl_res1 = Text("Retorna -1 (Seguro)", font_size=14, color=C_OK, weight=BOLD).move_to(tag_res1)
        sub_c1 = Text("Sin excepciones de puntero", font_size=12, color=C_APAGADO).move_to([xs[0], -1.8, 0])

        self.play(c1[0].animate.set_stroke(C_ACTIVO, width=3), FadeIn(txt_c1_op), FadeIn(box_null), FadeIn(lbl_null), run_time=0.6)
        self.play(FadeIn(tag_res1), FadeIn(lbl_res1), FadeIn(sub_c1), run_time=0.6)
        self.play(c1[0].animate.set_stroke(GRAY_B, width=2), run_time=0.3)

        pie_c1 = self.texto_inf("get(k) verifica nodo == nullptr y aborta la búsqueda en O(1) de forma segura.", C_OK)
        self.play(Transform(pie, pie_c1), run_time=0.4)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 3. CASO 2: UN SOLO ELEMENTO (0:17 - 0:27)
        # -------------------------------------------------------------
        txt_c2_op = Text("pop_back() / move_to_front()", font_size=14, color=WHITE).move_to([xs[1], 0.8, 0])
        nodo_unico = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.75, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=1).move_to([xs[1], 0.0, 0])
        lbl_n_u = Text("Key: 1 | V: 10", font_size=14, color=WHITE).move_to(nodo_unico)

        ptr_ht = Text("head == tail", font_size=13, color=C_ACTIVO, weight=BOLD).move_to([xs[1], -0.65, 0])
        tag_res2 = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.55, stroke_color=C_OK, fill_color="#0a2618", fill_opacity=1).move_to([xs[1], -1.2, 0])
        lbl_res2 = Text("head = tail = nullptr", font_size=14, color=C_OK, weight=BOLD).move_to(tag_res2)
        sub_c2 = Text("Evita referencias colgantes", font_size=12, color=C_APAGADO).move_to([xs[1], -1.8, 0])

        self.play(c2[0].animate.set_stroke(C_ACTIVO, width=3), FadeIn(txt_c2_op), FadeIn(nodo_unico), FadeIn(lbl_n_u), FadeIn(ptr_ht), run_time=0.6)
        self.play(FadeIn(tag_res2), FadeIn(lbl_res2), FadeIn(sub_c2), run_time=0.6)
        self.play(c2[0].animate.set_stroke(GRAY_B, width=2), run_time=0.3)

        pie_c2 = self.texto_inf("Si head == tail, pop_back() limpia ambos punteros a nullptr simultáneamente.", C_OK)
        self.play(Transform(pie, pie_c2), run_time=0.4)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 4. CASO 3: UPDATE DE CLAVE EXISTENTE (0:27 - 0:37)
        # -------------------------------------------------------------
        txt_c3_op = Text("put(2, 99) -> clave repetida", font_size=14, color=WHITE).move_to([xs[2], 0.8, 0])
        
        # Mini lista previa [2, 1]
        n_a = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.6, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=1).move_to([xs[2] - 0.9, 0.05, 0])
        t_a = Text("K:2 | 20", font_size=12, color=YELLOW).move_to(n_a)
        n_b = RoundedRectangle(corner_radius=0.08, width=1.4, height=0.6, stroke_color=C_NODO, fill_color="#0f2a33", fill_opacity=1).move_to([xs[2] + 0.9, 0.05, 0])
        t_b = Text("K:1 | 10", font_size=12, color=WHITE).move_to(n_b)
        mini_arr = DoubleArrow(n_a.get_right(), n_b.get_left(), buff=0.05, stroke_width=2, color=GRAY_B, tip_length=0.12)
        grupo_c3 = VGroup(n_a, t_a, n_b, t_b, mini_arr)

        self.play(c3[0].animate.set_stroke(C_ACTIVO, width=3), FadeIn(txt_c3_op), FadeIn(grupo_c3), run_time=0.6)

        # Muta a 99
        t_a_mut = Text("K:2 | 99", font_size=12, color=C_OK, weight=BOLD).move_to(n_a)
        self.play(Transform(t_a, t_a_mut), n_a.animate.set_stroke(C_OK, width=3.5), run_time=0.5)

        tag_res3 = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.55, stroke_color=C_OK, fill_color="#0a2618", fill_opacity=1).move_to([xs[2], -1.2, 0])
        lbl_res3 = Text("Mutación In-Place", font_size=14, color=C_OK, weight=BOLD).move_to(tag_res3)
        sub_c3 = Text("No desaloja ningún elemento", font_size=12, color=C_APAGADO).move_to([xs[2], -1.8, 0])

        self.play(FadeIn(tag_res3), FadeIn(lbl_res3), FadeIn(sub_c3), run_time=0.5)
        self.play(c3[0].animate.set_stroke(GRAY_B, width=2), run_time=0.3)

        pie_c3 = self.texto_inf("put() sobre clave existente sobreescribe su valor y va a Head sin alterar el tamaño.", C_ACTIVO)
        self.play(Transform(pie, pie_c3), run_time=0.4)
        self.wait(3.5)