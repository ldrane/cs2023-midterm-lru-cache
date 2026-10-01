"""
escenas_ilustrativas.py - Escenas conceptuales del video (Manim Community v0.21.0)

Son las escenas que NO salen del trace porque explican ideas generales
(caché, LRU/MRU, comparaciones, complejidad). Las que muestran la estructura
funcionando (bloques 5, 6, 7, 9 y 10) estan en escena.py y si usan el trace.

Uso (desde la raiz del repositorio):
    manim -pqh animation/escenas_ilustrativas.py Bloque01_Cache
    manim -pqh animation/escenas_ilustrativas.py Bloque02_LRU_MRU
    manim -pqh animation/escenas_ilustrativas.py Bloque03_UnaSolaEstructura
    manim -pqh animation/escenas_ilustrativas.py Bloque04_TDA
    manim -pqh animation/escenas_ilustrativas.py Bloque08_Comparativa
    manim -pqh animation/escenas_ilustrativas.py Bloque11_Complejidad

Variable opcional:  LRU_SPEED=1.3  (>1 = mas lento, <1 = mas rapido)
"""
import os

import numpy as np
from manim import *

VELOCIDAD = float(os.environ.get("LRU_SPEED", "1.0"))

# >>> EDITAR: datos de la tarjeta final <<<
INTEGRANTES = ["Integrante 1", "Integrante 2", "Integrante 3"]
CURSO = "CS2023 - Algoritmos y Estructuras de Datos  |  2026-2"

# Misma paleta que escena.py: MRU verde, LRU rojo, resaltado amarillo
C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_NODO = BLUE_C
C_APAGADO = GRAY_B


class Base(Scene):
    def rt(self, t):
        return t * VELOCIDAD

    def esperar(self, t):
        self.wait(self.rt(t))

    def poner_titulo(self, texto):
        t = Text(texto, font_size=40, color=YELLOW).to_edge(UP, buff=0.35)
        self.play(FadeIn(t, shift=DOWN * 0.2), run_time=self.rt(0.6))
        return t

    def caja(self, texto, w, h, color=C_NODO, size=24, fill="#0f2a33"):
        r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color,
                             stroke_width=3, fill_color=fill, fill_opacity=1)
        t = Text(texto, font_size=size)
        if t.width > w - 0.3:
            t.scale_to_fit_width(w - 0.3)
        t.move_to(r)
        return VGroup(r, t)

    def texto_inf(self, txt, color=WHITE, y=-3.3, size=28):
        t = Text(txt, font_size=size, color=color)
        if t.width > 12.8:
            t.scale_to_fit_width(12.8)
        return t.move_to([0, y, 0])

    def cambiar_texto(self, viejo, nuevo, dur=0.5):
        self.play(FadeTransform(viejo, nuevo), run_time=self.rt(dur))
        return nuevo


# =====================================================================
# Bloque 1 - Introduccion al cache (0:00 - 0:20)
# =====================================================================
class Bloque01_Cache(Base):
    def construct(self):
        self.poner_titulo("¿Qué es una caché?")

        cpu = self.caja("CPU / Servidor", 2.6, 1.4, BLUE_C).move_to([-5.0, -0.2, 0])
        cache = self.caja("Memoria Caché", 2.6, 1.0, C_OK).move_to([-0.6, 1.4, 0])
        sub_cache = Text("rápida, pero pequeña", font_size=20, color=C_APAGADO).next_to(cache, DOWN, buff=0.12)
        disco = self.caja("Base de datos / Disco", 3.6, 2.4, C_MAL).move_to([4.6, -0.6, 0])
        sub_disco = Text("lento, pero enorme", font_size=20, color=C_APAGADO).next_to(disco, DOWN, buff=0.12)

        self.play(FadeIn(cpu), run_time=self.rt(0.6))
        self.play(FadeIn(cache), FadeIn(sub_cache), run_time=self.rt(0.7))
        self.play(FadeIn(disco), FadeIn(sub_disco), run_time=self.rt(0.7))
        self.esperar(2.0)

        # Cache HIT: camino corto y rapido
        hit = Arrow(cpu.get_right() + UP * 0.3, cache.get_left(), buff=0.1, color=C_OK, stroke_width=5)
        lbl_hit = Text("Cache HIT: respuesta rápida", font_size=22, color=C_OK).move_to([-3.4, 2.2, 0])
        lbl_hit.set_z_index(2)
        punto = Dot(color=WHITE, radius=0.12).move_to(hit.get_start())
        self.play(GrowArrow(hit), FadeIn(lbl_hit), run_time=self.rt(0.8))
        self.add(punto)
        self.play(punto.animate.move_to(hit.get_end()), run_time=self.rt(0.5))
        self.play(punto.animate.move_to(hit.get_start()), run_time=self.rt(0.5))
        self.esperar(1.2)

        # Cache MISS: camino largo y costoso
        miss = Arrow(cpu.get_right() + DOWN * 0.3, disco.get_left(), buff=0.1, color=C_MAL, stroke_width=5)
        lbl_miss = Text("Cache MISS: acceso lento y costoso", font_size=22, color=C_MAL).move_to([-0.6, -1.2, 0])
        self.play(GrowArrow(miss), FadeIn(lbl_miss), run_time=self.rt(0.8))
        self.play(punto.animate.move_to(miss.get_end()), run_time=self.rt(2.2))
        self.play(punto.animate.move_to(miss.get_start()), run_time=self.rt(2.2))
        self.esperar(1.2)

        cap = self.texto_inf("Caché: almacenamiento temporal de capacidad fija N", C_ACTIVO)
        self.play(FadeIn(cap, shift=UP * 0.2), Circumscribe(cache, color=C_ACTIVO), run_time=self.rt(1.0))
        self.esperar(5.0)


# =====================================================================
# Bloque 2 - Concepto de LRU y MRU (0:20 - 0:40)
# =====================================================================
class Bloque02_LRU_MRU(Base):
    def construir_carta(self, letra, color):
        r = RoundedRectangle(corner_radius=0.12, width=2.1, height=1.1, stroke_color=color,
                             stroke_width=4, fill_color="#0f2a33", fill_opacity=1)
        return VGroup(r, Text(letra, font_size=44, color=color))

    def construct(self):
        self.poner_titulo("Política de desalojo: LRU")

        xs = [-3.2, 0.0, 3.2]
        y = 0.1
        ranuras = VGroup(*[Rectangle(width=2.6, height=1.5, stroke_color=GRAY, stroke_width=2).move_to([x, y, 0])
                           for x in xs])
        lbl_mru = Text("MRU (Head)\nmás reciente", font_size=24, color=C_OK, line_spacing=0.8)
        lbl_mru.next_to(ranuras[0], UP, buff=0.3)
        lbl_lru = Text("LRU (Tail)\ncandidato a expulsión", font_size=24, color=C_MAL, line_spacing=0.8)
        lbl_lru.next_to(ranuras[2], UP, buff=0.3)
        self.play(FadeIn(ranuras), run_time=self.rt(0.7))
        self.play(FadeIn(lbl_mru), FadeIn(lbl_lru), run_time=self.rt(0.8))

        A = self.construir_carta("A", BLUE_C).move_to([xs[0], y, 0])
        B = self.construir_carta("B", TEAL).move_to([xs[1], y, 0])
        C = self.construir_carta("C", PURPLE_B).move_to([xs[2], y, 0])
        self.play(LaggedStart(FadeIn(A, shift=DOWN * 0.3), FadeIn(B, shift=DOWN * 0.3),
                              FadeIn(C, shift=DOWN * 0.3), lag_ratio=0.35), run_time=self.rt(1.4))

        cap = self.texto_inf("Head = MRU (más reciente)   |   Tail = LRU (candidato a expulsión)", WHITE, size=26)
        self.play(FadeIn(cap), run_time=self.rt(0.6))
        self.esperar(2.0)

        # 1) Se usa C -> pasa a ser la mas reciente
        cap = self.cambiar_texto(cap, self.texto_inf("Se usa C: pasa a ser la más reciente (MRU)", C_ACTIVO))
        self.play(Circumscribe(C, color=C_ACTIVO), run_time=self.rt(0.8))
        self.play(C.animate.move_to([xs[0], y, 0]), A.animate.move_to([xs[1], y, 0]),
                  B.animate.move_to([xs[2], y, 0]), run_time=self.rt(1.2))
        self.esperar(1.5)

        # 2) Cache llena: entra D y se expulsa la LRU (B)
        cap = self.cambiar_texto(cap, self.texto_inf("Caché llena: entra D y se expulsa la menos reciente (B)", C_MAL))
        D = self.construir_carta("D", ORANGE).move_to([-6.2, y, 0])
        self.play(FadeIn(D, shift=RIGHT * 0.4), run_time=self.rt(0.7))
        self.play(B[0].animate.set_stroke(C_MAL, width=7), run_time=self.rt(0.6))
        self.esperar(0.6)
        self.play(FadeOut(B, shift=RIGHT * 1.5), run_time=self.rt(0.9))
        self.play(D.animate.move_to([xs[0], y, 0]), C.animate.move_to([xs[1], y, 0]),
                  A.animate.move_to([xs[2], y, 0]), run_time=self.rt(1.2))
        self.esperar(1.0)

        cap = self.cambiar_texto(cap, self.texto_inf("LRU descarta siempre lo que lleva más tiempo sin usarse", WHITE))
        self.esperar(3.0)


# =====================================================================
# Bloque 3 - Por que no una sola estructura (0:40 - 1:00)
# =====================================================================
class Bloque03_UnaSolaEstructura(Base):
    def construct(self):
        self.poner_titulo("¿Por qué no usar una sola estructura?")

        x_est, x_bus, x_reo = -6.6, 1.6, 5.3

        def celda_izq(txt, y, color=WHITE, size=26):
            t = Text(txt, font_size=size, color=color)
            return t.move_to([x_est + t.width / 2, y, 0])

        def celda(txt, x, y, color=WHITE, size=26):
            return Text(txt, font_size=size, color=color).move_to([x, y, 0])

        cab = VGroup(celda_izq("Estructura", 1.8, C_APAGADO, 24),
                     celda("Buscar", x_bus, 1.8, C_APAGADO, 24),
                     celda("Reordenar por uso", x_reo, 1.8, C_APAGADO, 24))
        linea = Line([-6.8, 1.45, 0], [6.8, 1.45, 0], color=GRAY, stroke_width=2)
        self.play(FadeIn(cab), Create(linea), run_time=self.rt(0.8))

        filas_datos = [
            ("Arreglo", ("O(N)", C_MAL), ("O(N)", C_MAL)),
            ("Lista doblemente enlazada sola", ("O(N)", C_MAL), ("O(1)*", C_OK)),
            ("Tabla hash sola", ("O(1) promedio", C_OK), ("No guarda orden", C_MAL)),
            ("Hash + lista (LRU Cache)", ("O(1) promedio", C_OK), ("O(1)", C_OK)),
        ]
        filas = []
        for i, (nombre, (b, cb), (r, cr)) in enumerate(filas_datos):
            y = 0.8 - i * 0.9
            fila = VGroup(celda_izq(nombre, y), celda(b, x_bus, y, cb), celda(r, x_reo, y, cr))
            filas.append(fila)
            self.play(FadeIn(fila, shift=RIGHT * 0.3), run_time=self.rt(0.7))
            self.esperar(2.4 if i < 3 else 1.0)

        marco = SurroundingRectangle(filas[3], color=C_OK, buff=0.18, corner_radius=0.1)
        self.play(Create(marco), run_time=self.rt(0.7))
        nota = Text("* si ya se tiene el nodo", font_size=22, color=C_APAGADO).move_to([-4.6, -2.75, 0])
        self.play(FadeIn(nota), run_time=self.rt(0.5))
        cap = self.texto_inf("Necesitamos buscar y reordenar en tiempo constante", C_ACTIVO, y=-3.4)
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=self.rt(0.8))
        self.esperar(5.0)


# =====================================================================
# Bloque 4 - Definicion formal del TDA (1:00 - 1:20)
# =====================================================================
class Bloque04_TDA(Base):
    def tarjeta(self, firma, lineas, y, color, alto=1.5):
        r = RoundedRectangle(corner_radius=0.15, width=12.2, height=alto, stroke_color=color,
                             stroke_width=3, fill_color="#0f2a33", fill_opacity=1)
        r.move_to([0, y, 0])
        f = Text(firma, font_size=38, color=YELLOW)
        d = VGroup(*[Text(l, font_size=22) for l in lineas]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        g = VGroup(f, d).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g.move_to(r.get_center()).align_to(r, LEFT).shift(RIGHT * 0.5)
        return VGroup(r, g)

    def construct(self):
        self.poner_titulo("TDA: LRU Cache")
        sub = Text("Tipo de Dato Abstracto asociativo de capacidad fija", font_size=26, color=C_APAGADO)
        sub.move_to([0, 2.35, 0])
        self.play(FadeIn(sub), run_time=self.rt(0.7))
        self.esperar(1.5)

        t_get = self.tarjeta("get(key)", ["devuelve el valor de la clave, o -1 si no existe",
                                          "si existe, la clave pasa a ser la más reciente (MRU)"],
                             1.0, C_OK, alto=1.9)
        self.play(FadeIn(t_get, shift=UP * 0.3), run_time=self.rt(0.9))
        self.esperar(4.0)

        t_put = self.tarjeta("put(key, value)", ["inserta o actualiza; la clave pasa a ser la más reciente"],
                             -0.9, BLUE_C)
        self.play(FadeIn(t_put, shift=UP * 0.3), run_time=self.rt(0.9))
        self.esperar(4.0)

        inv = VGroup(
            Text("Invariante:  tamaño ≤ capacidad", font_size=30, color=C_ACTIVO),
            Text("Si se excede, se expulsa la clave menos reciente (LRU)", font_size=24),
        ).arrange(DOWN, buff=0.15)
        marco = SurroundingRectangle(inv, color=C_ACTIVO, buff=0.3, corner_radius=0.15)
        VGroup(marco, inv).move_to([0, -2.5, 0])
        self.play(Create(marco), FadeIn(inv), run_time=self.rt(1.0))
        self.esperar(6.0)


# =====================================================================
# Bloque 8 - Busqueda secuencial vs. LRU Cache (2:50 - 3:10)
# =====================================================================
class Bloque08_Comparativa(Base):
    def cuadro(self, txt, x, y, w=0.72, h=0.6, size=22, color=GRAY_B):
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5)
        return VGroup(r, Text(str(txt), font_size=size)).move_to([x, y, 0])

    def contador(self, n, x, y=-2.45):
        return Text(f"Pasos: {n}", font_size=30, color=C_ACTIVO).move_to([x, y, 0])

    def construct(self):
        self.poner_titulo("Búsqueda secuencial vs. LRU Cache")
        div = Line([0, 2.6, 0], [0, -2.9, 0], color=GRAY, stroke_width=2)
        h_izq = Text("Búsqueda secuencial", font_size=26, color=C_MAL).move_to([-3.5, 2.5, 0])
        h_der = Text("LRU Cache (hash + lista)", font_size=26, color=C_OK).move_to([3.5, 2.5, 0])
        b_izq = Text("Buscar la clave 8", font_size=24).move_to([-3.5, 1.7, 0])
        b_der = Text("Buscar la clave 8", font_size=24).move_to([3.5, 1.7, 0])
        self.play(Create(div), FadeIn(h_izq), FadeIn(h_der), run_time=self.rt(0.8))
        self.play(FadeIn(b_izq), FadeIn(b_der), run_time=self.rt(0.5))

        # ---- Izquierda: recorrido uno por uno (peor caso: el ultimo)
        claves = [5, 2, 9, 4, 7, 1, 6, 8]
        celdas = [self.cuadro(k, -6.4 + i * 0.8, 0.5) for i, k in enumerate(claves)]
        self.play(FadeIn(VGroup(*celdas)), run_time=self.rt(0.6))
        flecha = Triangle(color=C_ACTIVO, fill_opacity=1).scale(0.15).move_to([-6.4, -0.15, 0])
        cnt = self.contador(1, -3.5)
        self.play(FadeIn(flecha), FadeIn(cnt), run_time=self.rt(0.4))
        for i in range(len(claves)):
            if i > 0:
                self.play(flecha.animate.move_to([-6.4 + i * 0.8, -0.15, 0]), run_time=self.rt(0.32))
                nuevo = self.contador(i + 1, -3.5)
                self.remove(cnt)
                self.add(nuevo)
                cnt = nuevo
            self.play(celdas[i][0].animate.set_stroke(C_OK if claves[i] == 8 else C_ACTIVO, width=5),
                      run_time=self.rt(0.15))
        self.play(Circumscribe(celdas[-1], color=C_OK), run_time=self.rt(0.6))
        nota_izq = Text("con N elementos: hasta N pasos", font_size=22, color=C_MAL).move_to([-3.5, -3.0, 0])
        self.play(FadeIn(nota_izq), run_time=self.rt(0.5))
        self.esperar(1.2)

        # ---- Derecha: bucket directo y un salto al nodo
        m = 7
        buckets = [self.cuadro("", 1.3 + i * 0.8, 0.7, w=0.7, h=0.5) for i in range(m)]
        idx = [Text(str(i), font_size=16, color=C_APAGADO).move_to([1.3 + i * 0.8, 1.1, 0]) for i in range(m)]
        self.play(FadeIn(VGroup(*buckets)), FadeIn(VGroup(*idx)), run_time=self.rt(0.6))
        nodos = [self.caja(f"Key: {k}", 1.5, 0.7, C_NODO, 20).move_to([x, -1.2, 0])
                 for k, x in zip([8, 3, 5], [2.1, 3.9, 5.7])]
        self.play(FadeIn(VGroup(*nodos)), run_time=self.rt(0.6))

        cnt_d = self.contador(0, 3.5)
        self.play(FadeIn(cnt_d), run_time=self.rt(0.3))
        formula = Text("8 % 7 = 1", font_size=26, color=C_ACTIVO).move_to([4.0, 0.0, 0])
        self.play(FadeIn(formula), buckets[1][0].animate.set_stroke(C_ACTIVO, width=5), run_time=self.rt(0.8))
        nuevo = self.contador(1, 3.5); self.remove(cnt_d); self.add(nuevo); cnt_d = nuevo
        self.esperar(0.6)
        salto = Arrow(buckets[1].get_bottom(), nodos[0].get_top(), buff=0.05, color=TEAL,
                      stroke_width=4)
        self.play(GrowArrow(salto), nodos[0][0].animate.set_stroke(C_OK, width=6), run_time=self.rt(0.8))
        nuevo = self.contador(2, 3.5); self.remove(cnt_d); self.add(nuevo); cnt_d = nuevo
        nota_der = Text("pocos pasos, sin importar N", font_size=22, color=C_OK).move_to([3.5, -3.0, 0])
        self.play(FadeIn(nota_der), run_time=self.rt(0.5))
        self.esperar(6.0)


# =====================================================================
# Bloque 11 - Complejidad y cierre (4:50 - 5:20)
# =====================================================================
class Bloque11_Complejidad(Base):
    def construct(self):
        self.poner_titulo("Análisis de complejidad  (N = capacidad)")

        x_op, x_prom, x_peor = -6.6, 1.2, 4.6

        def izq(txt, y, color=WHITE, size=28):
            t = Text(txt, font_size=size, color=color)
            return t.move_to([x_op + t.width / 2, y, 0])

        def cen(txt, x, y, color=WHITE, size=30):
            return Text(txt, font_size=size, color=color).move_to([x, y, 0])

        cab = VGroup(izq("Operación", 2.3, C_APAGADO, 26), cen("Caso promedio", x_prom, 2.3, C_APAGADO, 26),
                     cen("Peor caso", x_peor, 2.3, C_APAGADO, 26))
        linea = Line([-6.8, 1.95, 0], [6.8, 1.95, 0], color=GRAY, stroke_width=2)
        self.play(FadeIn(cab), Create(linea), run_time=self.rt(0.8))

        datos = [
            ("get(key)", "O(1)", "O(N)"),
            ("put(key, value)", "O(1)", "O(N)"),
            ("put con desalojo", "O(1)", "O(N)"),
            ("move_to_front / pop_back", "O(1)", "O(1)"),
        ]
        celdas_peor = []
        for i, (op, prom, peor) in enumerate(datos):
            y = 1.3 - i * 0.9
            c_peor = C_MAL if peor == "O(N)" else C_OK
            f = VGroup(izq(op, y), cen(prom, x_prom, y, C_OK), cen(peor, x_peor, y, c_peor))
            celdas_peor.append(f[2])
            self.play(FadeIn(f, shift=RIGHT * 0.3), run_time=self.rt(0.6))
            self.esperar(1.4)

        nota = self.texto_inf("Peor caso: todas las claves caen en el mismo bucket y se recorre la cadena",
                              C_MAL, y=-2.3, size=24)
        self.play(FadeIn(nota, shift=UP * 0.2),
                  *[Indicate(c, color=C_MAL) for c in celdas_peor[:3]], run_time=self.rt(1.2))
        self.esperar(3.5)
        nota2 = self.texto_inf("Mover un nodo y quitar la cola solo cambian punteros: siempre O(1)",
                               C_OK, y=-2.3, size=24)
        nota = self.cambiar_texto(nota, nota2)
        self.play(Indicate(celdas_peor[3], color=C_OK), run_time=self.rt(0.8))
        self.esperar(2.5)

        esp = self.texto_inf("Espacio total: O(N)", C_ACTIVO, y=-3.2, size=32)
        self.play(FadeIn(esp, shift=UP * 0.2), run_time=self.rt(0.8))
        self.esperar(4.0)

        # ---- tarjeta final
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=self.rt(0.8))
        t1 = Text("LRU Cache", font_size=64, color=YELLOW).move_to([0, 1.6, 0])
        t2 = Text("get y put en O(1) promedio", font_size=32, color=C_OK).move_to([0, 0.5, 0])
        t3 = Text(CURSO, font_size=24, color=C_APAGADO).move_to([0, -0.8, 0])
        t4 = Text("   ·   ".join(INTEGRANTES), font_size=26).move_to([0, -1.6, 0])
        if t4.width > 12.5:
            t4.scale_to_fit_width(12.5)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=self.rt(0.8))
        self.play(FadeIn(t2), run_time=self.rt(0.6))
        self.play(FadeIn(t3), FadeIn(t4), run_time=self.rt(0.6))
        self.esperar(4.5)
