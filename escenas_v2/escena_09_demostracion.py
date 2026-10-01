"""
escenas_v2/escena_09_demostracion.py
Escena 9: Demostración técnica de operaciones y ciclo de vida de la LRU Cache.
Estilo: Presentación académica de Algoritmos y Estructuras de Datos.
Hash íntegro: k:1, k:4 y k:3 siempre visibles; get(2) evaluado en zona independiente.
Duración calibrada: ~45 segundos.
"""

from manim import *
import numpy as np

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_NODO = BLUE_C
C_APAGADO = GRAY_B
C_ENTRADA = TEAL

Y_HASH = 1.30
Y_LISTA = -0.80
DX_SLOT = 3.3


class Escena09Demostracion(Scene):
    def pos_nodo(self, slot, total=3):
        return np.array([(slot - (total - 1) / 2) * DX_SLOT, Y_LISTA, 0])

    def crear_nodo(self, k, v):
        caja = RoundedRectangle(
            corner_radius=0.12, width=2.4, height=1.15,
            stroke_color=C_NODO, stroke_width=2.5,
            fill_color="#0f2a33", fill_opacity=1
        )
        tk = Text(f"Key: {k}", font_size=20, color=YELLOW, weight=BOLD)
        tv = Text(f"Val: {v}", font_size=18, color=WHITE)
        txts = VGroup(tk, tv).arrange(DOWN, buff=0.1).move_to(caja)
        return VGroup(caja, txts)

    def crear_tarjeta_hash(self, k):
        caja = RoundedRectangle(
            corner_radius=0.08, width=1.5, height=0.46,
            stroke_color=C_ENTRADA, stroke_width=2,
            fill_color="#092020", fill_opacity=1
        )
        t = Text(f"k:{k} -> ptr", font_size=15, color=WHITE).move_to(caja)
        return VGroup(caja, t)

    def texto_inf(self, txt, color=WHITE, y=-3.15, size=21):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # -------------------------------------------------------------
        # 1. ENCABEZADO ACADÉMICO FORMAL
        # -------------------------------------------------------------
        titulo = Text("Demostración Práctica: Ciclo de Vida y Evicción", font_size=36, color=YELLOW)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)

        caja_consola = RoundedRectangle(
            corner_radius=0.1, width=12.2, height=0.62,
            stroke_color=C_ACTIVO, stroke_width=2,
            fill_color="#14140c", fill_opacity=0.95
        ).move_to([0, 2.45, 0])

        txt_consola = Text("ESTADO: Capacidad = 3 | Estructura vacía", font_size=16, color=C_ACTIVO, font="Monospace")
        txt_consola.move_to(caja_consola)
        consola = VGroup(caja_consola, txt_consola)
        self.play(FadeIn(consola), run_time=0.6)

        tag_hash = Text("TABLA HASH (Acceso directo O(1))", font_size=14, color=C_ENTRADA, weight=BOLD).move_to([0, 1.80, 0])
        tag_lista = Text("LISTA DOBLEMENTE ENLAZADA (Historial temporal)", font_size=14, color=C_NODO, weight=BOLD).move_to([0, 0.15, 0])
        self.play(FadeIn(tag_hash), FadeIn(tag_lista), run_time=0.5)

        lbl_head = Text("MRU (Head)", font_size=16, color=C_OK, weight=BOLD).move_to([-3.3, Y_LISTA - 0.95, 0])
        lbl_tail = Text("LRU (Tail)", font_size=16, color=C_MAL, weight=BOLD).move_to([3.3, Y_LISTA - 0.95, 0])
        self.play(FadeIn(lbl_head), FadeIn(lbl_tail), run_time=0.5)

        pie = self.texto_inf("Inicialización: inserciones consecutivas de pares (clave, valor) en O(1).")
        self.play(FadeIn(pie), run_time=0.5)
        self.wait(1.5)

        # -------------------------------------------------------------
        # 2. INSERCIONES SUCESIVAS: put(1,10), put(2,20), put(3,30)
        # -------------------------------------------------------------
        nuevo_txt = Text("EJECUTANDO: put(1, 10) -> Inserta en Head y registra puntero", font_size=15, color=C_OK, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.4)
        n1 = self.crear_nodo(1, 10).move_to(self.pos_nodo(1))
        h1 = self.crear_tarjeta_hash(1).move_to([-2.6, Y_HASH, 0])
        self.play(FadeIn(n1, shift=DOWN * 0.3), FadeIn(h1), run_time=0.6)
        self.wait(0.6)

        nuevo_txt = Text("EJECUTANDO: put(2, 20) -> Nuevo Head (MRU). Nodo 1 se desplaza", font_size=15, color=C_OK, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.4)
        n2 = self.crear_nodo(2, 20).move_to(self.pos_nodo(0, 2))
        h2 = self.crear_tarjeta_hash(2).move_to([0, Y_HASH, 0])
        self.play(
            n1.animate.move_to(self.pos_nodo(1, 2)),
            FadeIn(n2, shift=DOWN * 0.3),
            FadeIn(h2),
            run_time=0.7
        )
        fl_21 = DoubleArrow(n2.get_right(), n1.get_left(), buff=0.1, stroke_width=2.5, color=C_APAGADO, tip_length=0.15)
        self.play(Create(fl_21), run_time=0.3)
        self.wait(0.6)

        nuevo_txt = Text("EJECUTANDO: put(3, 30) -> Capacidad llena (3/3). Orden: [3] -> [2] -> [1]", font_size=15, color=C_ACTIVO, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.4)
        n3 = self.crear_nodo(3, 30).move_to(self.pos_nodo(0, 3))
        h3 = self.crear_tarjeta_hash(3).move_to([2.6, Y_HASH, 0])
        self.play(
            FadeOut(fl_21),
            n2.animate.move_to(self.pos_nodo(1, 3)),
            n1.animate.move_to(self.pos_nodo(2, 3)),
            FadeIn(n3, shift=DOWN * 0.3),
            FadeIn(h3),
            run_time=0.8
        )
        fl_32 = DoubleArrow(n3.get_right(), n2.get_left(), buff=0.1, stroke_width=2.5, color=C_APAGADO, tip_length=0.15)
        fl_21 = DoubleArrow(n2.get_right(), n1.get_left(), buff=0.1, stroke_width=2.5, color=C_APAGADO, tip_length=0.15)
        self.play(Create(fl_32), Create(fl_21), run_time=0.4)

        pie_llena = self.texto_inf("Estructura al 100% de capacidad: Nodo 3 es MRU y Nodo 1 es candidato LRU.", C_ACTIVO)
        self.play(Transform(pie, pie_llena), run_time=0.4)
        self.wait(2.5)

        # -------------------------------------------------------------
        # 3. CONSULTA: get(1) -> CACHE HIT Y REASIGNACIÓN EN O(1)
        # -------------------------------------------------------------
        nuevo_txt = Text("EJECUTANDO: get(1) -> Cache Hit! move_to_front() promueve el nodo a la cabeza", font_size=15, color=C_OK, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.5)
        self.play(
            h1[0].animate.set_stroke(C_ACTIVO, width=4),
            n1[0].animate.set_stroke(C_ACTIVO, width=4),
            run_time=0.5
        )

        self.play(FadeOut(fl_32), FadeOut(fl_21), run_time=0.3)
        self.play(n1.animate.shift(UP * 1.0), run_time=0.5)
        self.play(
            n3.animate.move_to(self.pos_nodo(1, 3)),
            n2.animate.move_to(self.pos_nodo(2, 3)),
            run_time=0.7
        )
        self.play(n1.animate.move_to(self.pos_nodo(0, 3)), run_time=0.5)
        self.play(
            n1[0].animate.set_stroke(C_NODO, width=2.5),
            h1[0].animate.set_stroke(C_ENTRADA, width=2),
            run_time=0.3
        )

        fl_13 = DoubleArrow(n1.get_right(), n3.get_left(), buff=0.1, stroke_width=2.5, color=C_OK, tip_length=0.15)
        fl_32 = DoubleArrow(n3.get_right(), n2.get_left(), buff=0.1, stroke_width=2.5, color=C_OK, tip_length=0.15)
        self.play(Create(fl_13), Create(fl_32), run_time=0.4)

        pie_hit = self.texto_inf("Resultado de get(1): Nodo 1 asciende a MRU. El nodo 2 desciende a la cola (LRU).", C_OK)
        self.play(Transform(pie, pie_hit), run_time=0.4)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 4. DESALOJO POR CAPACIDAD: put(4, 40)
        # -------------------------------------------------------------
        nuevo_txt = Text("EJECUTANDO: put(4, 40) -> Capacidad agotada: pop_back() expulsa nodo 2 (LRU)", font_size=15, color=C_MAL, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.5)

        # Expulsión de la clave 2
        self.play(
            n2[0].animate.set_stroke(C_MAL, width=5),
            h2[0].animate.set_stroke(C_MAL, width=4),
            run_time=0.5
        )
        self.wait(0.5)

        self.play(
            FadeOut(fl_32),
            n2.animate.shift(DOWN * 1.3).fade(1),
            FadeOut(h2, shift=UP * 0.4),
            run_time=0.7
        )
        self.remove(n2, h2)

        # Entrada del nodo 4
        nuevo_txt = Text("EJECUTANDO: put(4, 40) -> Nodo 4 asignado en Head y registrado en Hash", font_size=15, color=C_OK, font="Monospace")
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        self.play(Transform(txt_consola, nuevo_txt), run_time=0.4)
        
        n4 = self.crear_nodo(4, 40).move_to(self.pos_nodo(0, 3) + UP * 1.0)
        h4 = self.crear_tarjeta_hash(4).move_to([0, Y_HASH, 0])

        self.play(
            n1.animate.move_to(self.pos_nodo(1, 3)),
            n3.animate.move_to(self.pos_nodo(2, 3)),
            FadeIn(h4),
            run_time=0.6
        )
        self.play(n4.animate.move_to(self.pos_nodo(0, 3)), FadeOut(fl_13), run_time=0.5)

        fl_41 = DoubleArrow(n4.get_right(), n1.get_left(), buff=0.1, stroke_width=2.5, color=C_OK, tip_length=0.15)
        fl_13 = DoubleArrow(n1.get_right(), n3.get_left(), buff=0.1, stroke_width=2.5, color=C_OK, tip_length=0.15)
        self.play(Create(fl_41), Create(fl_13), run_time=0.4)

        pie_evict = self.texto_inf("Evicción completada: Nodo 2 destruido. Nuevo orden: [4:40] -> [1:10] -> [3:30].", C_ACTIVO)
        self.play(Transform(pie, pie_evict), run_time=0.4)
        self.wait(2.5)

        # -------------------------------------------------------------
        # 5. VERIFICACIÓN: get(2) -> CACHE MISS (RETORNA -1)
        # h1 (k:1), h4 (k:4) y h3 (k:3) permanecen intactos en pantalla
        # La consulta se evalúa en el lateral izquierdo despejado (x = -4.9)
        # -------------------------------------------------------------
        nuevo_txt = Text("EJECUTANDO: get(2) -> Hash: clave no hallada -> Retorna -1 (Cache Miss)", font_size=15, color=C_MAL, font="Monospace", weight=BOLD)
        nuevo_txt.scale_to_fit_width(caja_consola.width - 0.9).move_to(caja_consola)
        
        self.play(
            Transform(txt_consola, nuevo_txt),
            caja_consola.animate.set_stroke(C_MAL, width=3),
            run_time=0.5
        )

        # Marco independiente en el extremo izquierdo libre, sin tocar a h1 (k:1)
        caja_miss_status = RoundedRectangle(
            corner_radius=0.08, width=2.0, height=0.68,
            stroke_color=C_MAL, stroke_width=2,
            fill_color="#240c0c", fill_opacity=0.95
        ).move_to([-4.85, Y_HASH, 0])
        
        t_miss_tit = Text("get(2)", font_size=13, color=WHITE, font="Monospace")
        t_miss_val = Text("nullptr (-1)", font_size=13, color=C_MAL, font="Monospace", weight=BOLD)
        txts_miss_status = VGroup(t_miss_tit, t_miss_val).arrange(DOWN, buff=0.06).move_to(caja_miss_status)
        grupo_miss = VGroup(caja_miss_status, txts_miss_status)

        self.play(FadeIn(grupo_miss, shift=RIGHT * 0.25), run_time=0.4)
        self.play(Indicate(caja_miss_status, color=C_MAL, scale_factor=1.05), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(grupo_miss), run_time=0.4)

        # Restaurar borde de consola al tono original
        self.play(caja_consola.animate.set_stroke(C_ACTIVO, width=2), run_time=0.3)

        pie_fin = self.texto_inf("get(2) = -1 confirma el desalojo correcto. La estructura mantiene integridad y tamaño <= 3.", C_OK, size=21)
        self.play(Transform(pie, pie_fin), run_time=0.5)
        self.wait(3.5)