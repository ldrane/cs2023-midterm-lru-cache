"""
escenas_v2/escena_10_casos_borde.py
Escena 10: Casos Borde y Robustez de Memoria en C++.
Duración calibrada: 66.5 segundos exactos sincronizados con la pista de audio.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_NODO = BLUE_C
C_APAGADO = GRAY_B
C_PANEL = "#0d1b2a"
C_ENTRADA = TEAL


class Escena10CasosBorde(Scene):
    def crear_tarjeta(self, titulo, ancho=6.0, alto=2.15):
        marco = RoundedRectangle(
            corner_radius=0.12, width=ancho, height=alto,
            stroke_color=GRAY_B, stroke_width=1.6,
            fill_color=C_PANEL, fill_opacity=0.94
        )
        t_tit = Text(titulo, font_size=15, color=YELLOW, weight=BOLD).next_to(marco.get_top(), DOWN, buff=0.11)
        sep = Line(
            marco.get_left() + RIGHT * 0.2, 
            marco.get_right() + LEFT * 0.2, 
            color=GRAY, stroke_width=1.0
        ).next_to(t_tit, DOWN, buff=0.07)
        return VGroup(marco, t_tit, sep)

    def texto_inf(self, txt, color=WHITE, y=-3.35, size=19):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.6:
            t.scale_to_fit_width(12.6)
        return t.move_to([0, y, 0])

    def construct(self):
        # =============================================================
        # 0:00 - 0:03.5 (3.5 s) | TÍTULO Y PRESENTACIÓN INICIAL
        # =============================================================
        titulo = Text("Casos Borde y Robustez de Memoria", font_size=34, color=YELLOW)
        titulo.to_edge(UP, buff=0.32)

        x_izq, x_der = -3.25, 3.25
        y_arr, y_abj = 1.35, -1.20

        c1 = self.crear_tarjeta("Caso 1: Caché Vacía").move_to([x_izq, y_arr, 0])
        c2 = self.crear_tarjeta("Caso 2: Capacidad = 1").move_to([x_der, y_arr, 0])
        c3 = self.crear_tarjeta("Caso 3: Clave Repetida").move_to([x_izq, y_abj, 0])
        c4 = self.crear_tarjeta("Caso 4: Colisión Hash (m = 7)").move_to([x_der, y_abj, 0])

        pie = self.texto_inf("Casos borde y robustez de memoria.")

        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), FadeIn(c4), FadeIn(pie), run_time=1.0)
        self.wait(1.7)  # Acumulado: 3.5s

        # =============================================================
        # 0:03.5 - 0:14.0 (10.5 s) | CASO 1: Caché Vacía
        # =============================================================
        c1_det = VGroup(
            Text("get(5) -> búsqueda en tabla vacía", font_size=13, color=WHITE),
            Text("head == tail == nullptr", font_size=13, color=C_MAL, font="Monospace"),
            Text("Retorna -1 seguro (sin violar segmento)", font_size=12, color=C_OK, weight=BOLD)
        ).arrange(DOWN, buff=0.10).move_to([x_izq, y_arr - 0.28, 0])

        self.play(
            c1[0].animate.set_stroke(C_ACTIVO, width=2.4),
            FadeIn(c1_det),
            Transform(pie, self.texto_inf("Caso 1: get devuelve -1 al instante sin tocar punteros nulos.", C_OK)),
            run_time=0.8
        )
        self.play(c1[0].animate.set_stroke(GRAY_B, width=1.6), run_time=0.2)
        self.wait(9.5)  # Acumulado: 14.0s

        # =============================================================
        # 0:14.0 - 0:21.0 (7.0 s) | CASO 2.1: Capacidad 1 (head == tail)
        # =============================================================
        c2_t1 = VGroup(
            Text("put(1, 10) con capacidad 1", font_size=13, color=WHITE),
            Text("head == tail  ->  [K:1 | V:10]", font_size=13, color=C_ACTIVO, font="Monospace"),
            Text("Un solo nodo representa ambos extremos", font_size=12, color=GRAY_B)
        ).arrange(DOWN, buff=0.10).move_to([x_der, y_arr - 0.28, 0])

        self.play(
            c2[0].animate.set_stroke(C_ACTIVO, width=2.4),
            FadeIn(c2_t1),
            Transform(pie, self.texto_inf("Caso 2: con capacidad uno, cabeza y cola son exactamente el mismo nodo.", C_OK)),
            run_time=0.8
        )
        self.play(c2[0].animate.set_stroke(GRAY_B, width=1.6), run_time=0.2)
        self.wait(6.0)  # Acumulado: 21.0s

        # =============================================================
        # 0:21.0 - 0:26.0 (5.0 s) | CASO 2.2: put(2, 20) -> EVICT
        # =============================================================
        c2_t2 = VGroup(
            Text("put(2, 20)  ->  EVICT clave 1", font_size=13, color=C_MAL, weight=BOLD),
            Text("pop_back() elimina el nodo 1", font_size=13, color=C_MAL, font="Monospace"),
            Text("Nuevo head == tail  ->  [K:2 | V:20]", font_size=12, color=C_OK)
        ).arrange(DOWN, buff=0.10).move_to([x_der, y_arr - 0.28, 0])

        self.play(
            Transform(c2_t1, c2_t2),
            Transform(pie, self.texto_inf("Al insertar el dos, el uno queda expulsado de inmediato.", C_ACTIVO)),
            run_time=0.6
        )
        self.wait(4.4)  # Acumulado: 26.0s

        # =============================================================
        # 0:26.0 - 0:34.0 (8.0 s) | CASO 2.3: get(1) MISS, get(2) ALREADY_HEAD
        # =============================================================
        c2_t3 = VGroup(
            Text("get(1) -> MISS (-1)", font_size=13, color=C_MAL, font="Monospace"),
            Text("get(2) -> HIT | ALREADY_HEAD", font_size=13, color=C_OK, font="Monospace"),
            Text("El 2 ya es la cabeza: 0 enlaces alterados", font_size=11, color=GRAY_B)
        ).arrange(DOWN, buff=0.08).move_to([x_der, y_arr - 0.28, 0])

        self.play(
            Transform(c2_t1, c2_t3),
            Transform(pie, self.texto_inf("El uno da MISS; get(2) no altera enlaces porque ya es la cabeza.", C_OK)),
            run_time=0.6
        )
        self.wait(7.4)  # Acumulado: 34.0s

        # =============================================================
        # 0:34.0 - 0:46.0 (12.0 s) | CASO 3: put(1, 99) Actualización In-Place
        # =============================================================
        c3_det = VGroup(
            Text("put(1, 99)  ->  clave existente", font_size=13, color=WHITE),
            Text("node->value = 99;  move_to_front(node);", font_size=13, color=YELLOW, font="Monospace"),
            Text("Sobreescribe el dato y va al frente", font_size=12, color=C_OK),
            Text("Sin expulsar a nadie: size se mantiene", font_size=12, color=C_OK, weight=BOLD)
        ).arrange(DOWN, buff=0.08).move_to([x_izq, y_abj - 0.28, 0])

        self.play(
            c3[0].animate.set_stroke(C_ACTIVO, width=2.4),
            FadeIn(c3_det),
            Transform(pie, self.texto_inf("Caso 3: put(1, 99) sobreescribe el dato y lo lleva al frente sin expulsar.", C_ACTIVO)),
            run_time=0.8
        )
        self.play(c3[0].animate.set_stroke(GRAY_B, width=1.6), run_time=0.2)
        self.wait(11.0)  # Acumulado: 46.0s

        # =============================================================
        # 0:46.0 - 0:52.0 (6.0 s) | CASO 4.1: Colisión Hash
        # =============================================================
        c4_t1 = VGroup(
            Text("1 % 7 == 1  y  8 % 7 == 1", font_size=13, color=WHITE),
            Text("Mismo bucket: Bucket[1]", font_size=13, color=C_ACTIVO, font="Monospace"),
            Text("Colisión resuelta por encadenamiento", font_size=12, color=GRAY_B)
        ).arrange(DOWN, buff=0.10).move_to([x_der, y_abj - 0.28, 0])

        self.play(
            c4[0].animate.set_stroke(C_ACTIVO, width=2.4),
            FadeIn(c4_t1),
            Transform(pie, self.texto_inf("Caso 4: colisión de la tabla; el uno y el ocho caen en el mismo bucket.", C_OK)),
            run_time=0.6
        )
        self.play(c4[0].animate.set_stroke(GRAY_B, width=1.6), run_time=0.2)
        self.wait(5.2)  # Acumulado: 52.0s

        # =============================================================
        # 0:52.0 - 0:56.5 (4.5 s) | CASO 4.2: Encadenamiento al inicio
        # =============================================================
        c4_t2 = VGroup(
            Text("put(8, 80) se encadena al inicio:", font_size=13, color=WHITE),
            Text("Bucket[1] -> [k:8] -> [k:1] -> nullptr", font_size=13, color=YELLOW, font="Monospace"),
            Text("Inserción O(1) al frente del bucket", font_size=12, color=C_OK)
        ).arrange(DOWN, buff=0.10).move_to([x_der, y_abj - 0.28, 0])

        self.play(
            Transform(c4_t1, c4_t2),
            Transform(pie, self.texto_inf("El ocho simplemente se encadena al inicio de la lista de ese casillero.", C_ACTIVO)),
            run_time=0.5
        )
        self.wait(4.0)  # Acumulado: 56.5s

        # =============================================================
        # 0:56.5 - 1:01.5 (5.0 s) | CASO 4.3: Recorrido y 2 PROBES
        # =============================================================
        c4_t3 = VGroup(
            Text("get(1): 2 PROBES (8 -> 1 HIT)", font_size=13, color=C_ACTIVO, weight=BOLD),
            Text("1° compara con [k:8] (No coincide)", font_size=12, color=GRAY_B),
            Text("2° compara con [k:1] (HIT!)", font_size=12, color=C_OK, weight=BOLD)
        ).arrange(DOWN, buff=0.08).move_to([x_der, y_abj - 0.28, 0])

        self.play(
            Transform(c4_t1, c4_t3),
            Transform(pie, self.texto_inf("Para buscar el uno recorremos la cadena: primero el ocho y luego el uno.", C_OK)),
            run_time=0.6
        )
        self.wait(4.4)  # Acumulado: 61.5s

        # =============================================================
        # 1:01.5 - 1:06.5 (5.0 s) | CASO 4.4: Cierre
        # =============================================================
        c4_t4 = VGroup(
            Text("get(1) resuelto correctamente", font_size=13, color=C_OK, font="Monospace"),
            Text("Sin alterar la lista doblemente enlazada", font_size=11, color=WHITE),
            Text("Toma un paso adicional, pero es exacto", font_size=11, color=C_OK, weight=BOLD)
        ).arrange(DOWN, buff=0.08).move_to([x_der, y_abj - 0.28, 0])

        self.play(
            Transform(c4_t1, c4_t4),
            Transform(pie, self.texto_inf("La búsqueda toma un paso adicional, pero el resultado sigue siendo exacto.", C_OK)),
            run_time=0.5
        )
        self.wait(4.5)  # Acumulado: 66.5s exactos