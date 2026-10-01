"""
escenas_v2/escena_05_06_estructura.py
Escena 5 y 6: Componentes y Unificación (Hash Table + Doubly Linked List).
Estructura limpia, sin textos cruzados y con tiempos desahogados (~40 segundos).
"""

from manim import *
import numpy as np

C_NODO = BLUE_C
C_ENTRADA = TEAL
C_ENLACE = GRAY_B
C_ACTIVO = YELLOW
C_OK = GREEN
C_MAL = RED
C_APAGADO = GRAY_B

ANCHO_BUCKET = 1.35
Y_BUCKETS = 2.15
Y_ENTRADA0 = 1.35
Y_LISTA = -0.95
DX_SLOT = 3.2


class Escena0506Estructura(Scene):
    def bx(self, b, m=7):
        return (b - (m - 1) / 2) * ANCHO_BUCKET

    def pos_bucket(self, b):
        return np.array([self.bx(b), Y_BUCKETS, 0])

    def pos_entrada(self, b):
        return np.array([self.bx(b), Y_ENTRADA0, 0])

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

    def crear_entrada_hash(self, k):
        caja = RoundedRectangle(
            corner_radius=0.08, width=1.0, height=0.45,
            stroke_color=C_ENTRADA, stroke_width=2,
            fill_color="#0d2626", fill_opacity=1
        )
        t = Text(f"k:{k}", font_size=16, color=WHITE).move_to(caja)
        return VGroup(caja, t)

    def texto_inf(self, txt, color=WHITE, y=-3.25, size=21):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO SUPERIOR DESPEJADO
        # -------------------------------------------------------------
        titulo = Text("Arquitectura: Tabla Hash + Lista Doble", font_size=38, color=YELLOW)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)

        # -------------------------------------------------------------
        # 2. BLOQUE SUPERIOR: TABLA HASH (Con etiqueta lateral izquierda)
        # -------------------------------------------------------------
        m = 7
        tag_hash = VGroup(
            Text("TABLA HASH", font_size=16, color=C_ACTIVO, weight=BOLD),
            Text("m = 7 buckets", font_size=13, color=C_APAGADO)
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([-5.6, Y_BUCKETS, 0])

        buckets = VGroup(*[
            Rectangle(width=ANCHO_BUCKET - 0.2, height=0.52, stroke_color=GRAY_B, stroke_width=2)
            .move_to(self.pos_bucket(b))
            for b in range(m)
        ])
        indices = VGroup(*[
            Text(str(b), font_size=15, color=GRAY_B).move_to(self.pos_bucket(b) + UP * 0.42)
            for b in range(m)
        ])
        grupo_hash = VGroup(tag_hash, buckets, indices)

        # -------------------------------------------------------------
        # 3. BLOQUE INFERIOR: LISTA DOBLE (Con etiqueta lateral izquierda)
        # -------------------------------------------------------------
        cap = 3
        tag_lista = VGroup(
            Text("LISTA DOBLE", font_size=16, color=C_NODO, weight=BOLD),
            Text("capacidad = 3", font_size=13, color=C_APAGADO)
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([-5.6, Y_LISTA, 0])

        ranuras = VGroup(*[
            Rectangle(width=2.5, height=1.35, stroke_color=GRAY, stroke_width=1.5, stroke_opacity=0.35)
            .move_to(self.pos_nodo(i))
            for i in range(cap)
        ])

        # Etiquetas MRU y LRU en la parte inferior, sin estorbar el centro
        lbl_head = Text("MRU (Head)", font_size=18, color=C_OK, weight=BOLD).next_to(ranuras[0], DOWN, buff=0.25)
        lbl_tail = Text("LRU (Tail)", font_size=18, color=C_MAL, weight=BOLD).next_to(ranuras[2], DOWN, buff=0.25)
        grupo_lista = VGroup(tag_lista, ranuras, lbl_head, lbl_tail)

        # Aparición limpia de las dos estructuras
        self.play(FadeIn(grupo_hash, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(grupo_lista, shift=UP * 0.2), run_time=0.8)

        pie = self.texto_inf("Arriba: acceso directo por clave.  Abajo: control estricto del orden temporal.")
        self.play(FadeIn(pie), run_time=0.6)
        self.wait(4.0)

        # -------------------------------------------------------------
        # 4. NODOS DE LA LISTA DOBLE Y FLECHAS PREV / NEXT
        # -------------------------------------------------------------
        nodo_3 = self.crear_nodo(3, 30).move_to(self.pos_nodo(0))  # Head (MRU)
        nodo_2 = self.crear_nodo(2, 20).move_to(self.pos_nodo(1))
        nodo_1 = self.crear_nodo(1, 10).move_to(self.pos_nodo(2))  # Tail (LRU)

        self.play(
            LaggedStart(
                FadeIn(nodo_3, shift=DOWN * 0.3),
                FadeIn(nodo_2, shift=DOWN * 0.3),
                FadeIn(nodo_1, shift=DOWN * 0.3),
                lag_ratio=0.3
            ),
            run_time=1.3
        )

        flecha_32 = DoubleArrow(
            nodo_3.get_right() + UP * 0.05, nodo_2.get_left() + UP * 0.05,
            buff=0.1, stroke_width=3, color=C_ENLACE, tip_length=0.18
        )
        flecha_21 = DoubleArrow(
            nodo_2.get_right() + UP * 0.05, nodo_1.get_left() + UP * 0.05,
            buff=0.1, stroke_width=3, color=C_ENLACE, tip_length=0.18
        )
        enlaces_lista = VGroup(flecha_32, flecha_21)
        self.play(Create(enlaces_lista), run_time=0.8)

        pie_nodos = self.texto_inf("Nodos enlazados con punteros prev y next: inserción y extracción en O(1).", C_OK)
        self.play(Transform(pie, pie_nodos), run_time=0.6)
        self.wait(4.5)

        # -------------------------------------------------------------
        # 5. UNIFICACIÓN: ENTRADAS HASH Y PUNTEROS DIRECTOS AL NODO
        # -------------------------------------------------------------
        ent_1 = self.crear_entrada_hash(1).move_to(self.pos_entrada(1))
        ent_2 = self.crear_entrada_hash(2).move_to(self.pos_entrada(2))
        ent_3 = self.crear_entrada_hash(3).move_to(self.pos_entrada(3))
        entradas_hash = VGroup(ent_1, ent_2, ent_3)

        self.play(
            LaggedStart(
                FadeIn(ent_1, shift=DOWN * 0.2),
                FadeIn(ent_2, shift=DOWN * 0.2),
                FadeIn(ent_3, shift=DOWN * 0.2),
                lag_ratio=0.3
            ),
            run_time=1.0
        )

        # Flechas que bajan en un canal central totalmente libre de textos
        ptr_1 = Arrow(ent_1.get_bottom(), nodo_1.get_top(), buff=0.1, stroke_width=2.5, color=C_ENTRADA, tip_length=0.18)
        ptr_2 = Arrow(ent_2.get_bottom(), nodo_2.get_top(), buff=0.1, stroke_width=2.5, color=C_ENTRADA, tip_length=0.18)
        ptr_3 = Arrow(ent_3.get_bottom(), nodo_3.get_top(), buff=0.1, stroke_width=2.5, color=C_ENTRADA, tip_length=0.18)
        punteros_hash = VGroup(ptr_1, ptr_2, ptr_3)

        pie_unif = self.texto_inf("Unificación: cada entrada de la tabla almacena un puntero directo al nodo (DoubleNode*).", C_ACTIVO)
        self.play(Transform(pie, pie_unif), Create(punteros_hash), run_time=1.2)
        self.wait(4.5)

        # -------------------------------------------------------------
        # 6. RESALTADO DEL SALTO EN O(1)
        # -------------------------------------------------------------
        self.play(
            Indicate(punteros_hash, color=C_ACTIVO, scale_factor=1.03),
            run_time=1.0
        )

        pie_fin = self.texto_inf("Resultado: localizamos cualquier nodo en O(1) promedio sin recorrer la lista.", C_OK, size=22)
        self.play(Transform(pie, pie_fin), run_time=0.6)
        self.wait(4.5)