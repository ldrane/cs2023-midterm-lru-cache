"""
escenas_v2/escena_07_punteros.py
Escena 7: El papel de los punteros y move_to_front paso a paso.
Clarificación gráfica de punteros (next y prev) y código sincronizado.
"""

from manim import *
import numpy as np

C_NODO = BLUE_C
C_ENLACE = GRAY_B
C_ACTIVO = YELLOW
C_OK = GREEN
C_MAL = RED
C_APAGADO = GRAY_B
C_CODIGO = "#80FFDB"

Y_LISTA = -0.55
DX_SLOT = 3.6


class Escena07Punteros(Scene):
    def pos_nodo(self, slot, cap=3):
        return np.array([(slot - (cap - 1) / 2) * DX_SLOT, Y_LISTA, 0])

    def crear_nodo(self, k, v):
        caja = RoundedRectangle(
            corner_radius=0.12, width=2.3, height=1.15,
            stroke_color=C_NODO, stroke_width=2.5,
            fill_color="#0f2a33", fill_opacity=1
        )
        tk = Text(f"Key: {k}", font_size=20, color=YELLOW, weight=BOLD)
        tv = Text(f"Val: {v}", font_size=18, color=WHITE)
        txts = VGroup(tk, tv).arrange(DOWN, buff=0.1).move_to(caja)
        return VGroup(caja, txts)

    def texto_inf(self, txt, color=WHITE, y=-3.3, size=21):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO PRINCIPAL
        # -------------------------------------------------------------
        titulo = Text("Operación interna: move_to_front(node)", font_size=38, color=YELLOW)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)

        # -------------------------------------------------------------
        # 2. ESTADO INICIAL [3, 2, 1] CON ETIQUETAS DE PUNTEROS
        # -------------------------------------------------------------
        cap = 3
        ranuras = VGroup(*[
            Rectangle(width=2.5, height=1.35, stroke_color=GRAY, stroke_width=1.5, stroke_opacity=0.35)
            .move_to(self.pos_nodo(i))
            for i in range(cap)
        ])

        lbl_head = Text("MRU (Head)", font_size=18, color=C_OK, weight=BOLD).next_to(ranuras[0], DOWN, buff=0.3)
        lbl_tail = Text("LRU (Tail)", font_size=18, color=C_MAL, weight=BOLD).next_to(ranuras[2], DOWN, buff=0.3)

        nodo_3 = self.crear_nodo(3, 30).move_to(self.pos_nodo(0))
        nodo_2 = self.crear_nodo(2, 20).move_to(self.pos_nodo(1))
        nodo_1 = self.crear_nodo(1, 10).move_to(self.pos_nodo(2))

        # Flechas de enlace iniciales
        arr_32 = DoubleArrow(nodo_3.get_right() + UP * 0.05, nodo_2.get_left() + UP * 0.05,
                             buff=0.12, stroke_width=3, color=C_ENLACE, tip_length=0.18)
        arr_21 = DoubleArrow(nodo_2.get_right() + UP * 0.05, nodo_1.get_left() + UP * 0.05,
                             buff=0.12, stroke_width=3, color=C_ENLACE, tip_length=0.18)
        enlaces_iniciales = VGroup(arr_32, arr_21)

        self.play(FadeIn(ranuras), FadeIn(lbl_head), FadeIn(lbl_tail), run_time=0.6)
        self.play(FadeIn(nodo_3), FadeIn(nodo_2), FadeIn(nodo_1), Create(enlaces_iniciales), run_time=0.9)

        pie = self.texto_inf("get(2): Localizado en O(1) por el Hash. Ahora reordenamos en la Lista.")
        self.play(FadeIn(pie), run_time=0.5)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 3. FASE 1: DESCONEXIÓN QUIRÚRGICA (EXPLICANDO NEXT Y PREV)
        # -------------------------------------------------------------
        self.play(nodo_2[0].animate.set_stroke(C_ACTIVO, width=5), run_time=0.5)

        caja_codigo = RoundedRectangle(
            corner_radius=0.1, width=12.0, height=0.68,
            stroke_color=C_CODIGO, stroke_width=2,
            fill_color="#081c1c", fill_opacity=0.95
        ).move_to([0, 2.15, 0])

        txt_paso1 = Text("Fase 1:  node->prev->next = node->next;   node->next->prev = node->prev;",
                         font_size=17, color=C_CODIGO, font="Monospace").move_to(caja_codigo)
        paso1_grupo = VGroup(caja_codigo, txt_paso1)

        # Desconectar enlaces y elevar el nodo 2 a una altura limpia
        self.play(FadeIn(paso1_grupo), FadeOut(enlaces_iniciales), run_time=0.6)
        self.play(nodo_2.animate.move_to([self.pos_nodo(1)[0], 0.95, 0]), run_time=0.8)

        # Puente directo entre nodo 3 y nodo 1 con etiqueta explícita
        arr_puente_31 = DoubleArrow(nodo_3.get_right() + UP * 0.05, nodo_1.get_left() + UP * 0.05,
                                    buff=0.15, stroke_width=3.5, color=C_ACTIVO, tip_length=0.2)
        lbl_puente = Text("Punteros puenteados (3 <-> 1)", font_size=14, color=C_ACTIVO).next_to(arr_puente_31, UP, buff=0.12)

        self.play(Create(arr_puente_31), FadeIn(lbl_puente), run_time=0.7)

        pie_fase1 = self.texto_inf("Los vecinos se puentean mutuamente. El nodo 2 queda aislado en memoria.", C_ACTIVO)
        self.play(Transform(pie, pie_fase1), run_time=0.5)
        self.wait(4.0)

        # -------------------------------------------------------------
        # 4. FASE 2: RECONEXIÓN EN LA CABEZA (HEAD / MRU)
        # -------------------------------------------------------------
        txt_paso2 = Text("Fase 2:  node->next = head;   head->prev = node;   head = node;",
                         font_size=17, color=C_OK, font="Monospace").move_to(caja_codigo)

        self.play(
            FadeOut(arr_puente_31), FadeOut(lbl_puente),
            Transform(txt_paso1, txt_paso2),
            caja_codigo.animate.set_stroke(C_OK),
            run_time=0.6
        )

        # 3 y 1 se corren a la derecha; 2 vuela a la columna 0
        self.play(
            nodo_3.animate.move_to(self.pos_nodo(1)),
            nodo_1.animate.move_to(self.pos_nodo(2)),
            nodo_2.animate.move_to([self.pos_nodo(0)[0], 0.95, 0]),
            run_time=1.0
        )
        self.play(nodo_2.animate.move_to(self.pos_nodo(0)), run_time=0.5)
        self.play(nodo_2[0].animate.set_stroke(C_NODO, width=2.5), run_time=0.3)

        # Nuevos enlaces reasignados
        arr_final_23 = DoubleArrow(nodo_2.get_right() + UP * 0.05, nodo_3.get_left() + UP * 0.05,
                                   buff=0.12, stroke_width=3, color=C_OK, tip_length=0.18)
        arr_final_31 = DoubleArrow(nodo_3.get_right() + UP * 0.05, nodo_1.get_left() + UP * 0.05,
                                   buff=0.12, stroke_width=3, color=C_OK, tip_length=0.18)
        enlaces_finales = VGroup(arr_final_23, arr_final_31)
        self.play(Create(enlaces_finales), run_time=0.7)

        pie_fase2 = self.texto_inf("Reconexión: El nodo 2 es la nueva cabeza (MRU). 3 y 1 mantienen su orden.", C_OK)
        self.play(Transform(pie, pie_fase2), run_time=0.5)
        self.wait(3.5)

        # -------------------------------------------------------------
        # 5. REMATE PEDAGÓGICO DE COMPLEJIDAD
        # -------------------------------------------------------------
        self.play(Indicate(enlaces_finales, color=C_ACTIVO, scale_factor=1.04), run_time=0.8)

        pie_fin = self.texto_inf("Solo 4 asignaciones de punteros: el reordenamiento es estrictamente O(1).", C_ACTIVO, size=22)
        self.play(Transform(pie, pie_fin), run_time=0.6)
        self.wait(4.0)