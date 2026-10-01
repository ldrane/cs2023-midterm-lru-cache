"""
escenas_v2/escena_04_tda.py
Escena 4: Definición formal del TDA LRU Cache y sus operaciones.
Duración calibrada: ~21 segundos.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_APAGADO = GRAY_B
C_METODO = BLUE_C


class Escena04TDA(Scene):
    def crear_tarjeta_metodo(self, firma, lineas, y, color_borde):
        caja = RoundedRectangle(
            corner_radius=0.12,
            width=12.2,
            height=1.45,
            stroke_color=color_borde,
            stroke_width=2.5,
            fill_color="#0d212d",
            fill_opacity=1
        ).move_to([0, y, 0])

        txt_firma = Text(firma, font_size=28, color=YELLOW, weight=BOLD)
        txt_desc = VGroup(*[
            Text(l, font_size=19, color=WHITE) for l in lineas
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        contenido = VGroup(txt_firma, txt_desc).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        
        # Ajuste de seguridad para que nunca toque los bordes
        if contenido.width > caja.width - 0.8:
            contenido.scale_to_fit_width(caja.width - 0.8)

        contenido.move_to(caja.get_center()).align_to(caja, LEFT).shift(RIGHT * 0.4)

        return VGroup(caja, contenido)

    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO Y SUBTÍTULO
        # -------------------------------------------------------------
        titulo = Text("TDA: LRU Cache", font_size=40, color=YELLOW)
        titulo.to_edge(UP, buff=0.42)
        
        sub = Text("Tipo de Dato Abstracto asociativo con capacidad fija K",
                   font_size=21, color=C_APAGADO).next_to(titulo, DOWN, buff=0.16)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), FadeIn(sub), run_time=0.7)
        self.wait(2.0)

        # -------------------------------------------------------------
        # 2. TARJETA GET(KEY)
        # -------------------------------------------------------------
        t_get = self.crear_tarjeta_metodo(
            "int get(int key)",
            [
                "• Retorna el valor si existe y promueve el nodo a MRU (Head).",
                "• Si no existe, retorna -1 (Cache Miss) sin alterar la estructura."
            ],
            y=1.15,
            color_borde=C_OK
        )
        self.play(FadeIn(t_get, shift=UP * 0.25), run_time=0.6)
        self.wait(3.5)

        # -------------------------------------------------------------
        # 3. TARJETA PUT(KEY, VALUE)
        # -------------------------------------------------------------
        t_put = self.crear_tarjeta_metodo(
            "void put(int key, int value)",
            [
                "• Inserta o actualiza el par (clave, valor) y lo promueve a MRU (Head).",
                "• Si la clave ya existe, muta su valor sin requerir un nuevo nodo."
            ],
            y=-0.45,
            color_borde=C_METODO
        )
        self.play(FadeIn(t_put, shift=UP * 0.25), run_time=0.6)
        self.wait(3.5)

        # -------------------------------------------------------------
        # 4. INVARIANTE ESTRUCTURAL Y DESALOJO (Ajustada en 2 renglones)
        # -------------------------------------------------------------
        caja_inv = RoundedRectangle(
            corner_radius=0.12,
            width=12.2,
            height=1.45,
            stroke_color=C_ACTIVO,
            stroke_width=2.5,
            fill_color="#262211",
            fill_opacity=0.85
        ).move_to([0, -2.1, 0])

        txt_inv1 = Text("Invariante:  tamaño  ≤  capacidad", font_size=24, color=C_ACTIVO, weight=BOLD)
        txt_inv2 = Text("Si size == capacidad y entra una nueva clave, se expulsa el nodo en la cola:",
                        font_size=18, color=WHITE)
        txt_inv3 = Text("pop_back()  +  map.erase(LRU)", font_size=18, color=YELLOW)

        grupo_textos = VGroup(txt_inv1, txt_inv2, txt_inv3).arrange(DOWN, buff=0.08)
        
        # Margen de seguridad interior
        if grupo_textos.width > caja_inv.width - 0.8:
            grupo_textos.scale_to_fit_width(caja_inv.width - 0.8)

        grupo_textos.move_to(caja_inv.get_center())
        tarjeta_invariante = VGroup(caja_inv, grupo_textos)

        self.play(FadeIn(tarjeta_invariante, shift=UP * 0.2), run_time=0.7)
        self.wait(4.5)