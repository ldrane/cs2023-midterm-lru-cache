"""
escena.py - Animacion de la LRU Cache con Manim Community v0.21.0

La animacion NO tiene valores escritos a mano: todo sale de trace/trace.jsonl,
que genera el programa en C++ (src/lru_cache.cpp) al ejecutar la estructura real.
Cada linea del trace trae, por operacion, los pasos (HASH, PROBE, HIT, MISS, UPDATE,
MOVE_TO_FRONT, EVICT, INSERT) y el estado completo resultante (lista + buckets).
Al final de cada operacion la escena comprueba que lo dibujado coincide con ese
estado; si no coincide, se corrige, asi el dibujo nunca se aparta del codigo real.

Uso (desde la raiz del repositorio):
    g++ -std=c++17 -O2 -o lru src/lru_cache.cpp
    ./lru > trace/trace.jsonl
    manim -pqh animation/escena.py Bloque09_Demostracion

Escenas disponibles (numeracion del guion):
    Bloque05_06_Estructura   componentes y unificacion (tabla hash + lista)
    Bloque07_Punteros        move_to_front paso a paso sobre un nodo intermedio
    Bloque09_Demostracion    put/get/evict con el caso principal
    Bloque10_CasosBorde      vacia, capacidad 1, clave existente, colision

Variables de entorno opcionales:
    LRU_TRACE=ruta/al/trace.jsonl   otro archivo de trace
    LRU_SPEED=1.3                   >1 = animacion mas lenta, <1 = mas rapida
"""
import json
import os

import numpy as np
from manim import *

RAIZ = os.path.dirname(os.path.abspath(__file__))
RUTA_TRACE = os.environ.get("LRU_TRACE", os.path.join(RAIZ, "..", "trace", "trace.jsonl"))
VELOCIDAD = float(os.environ.get("LRU_SPEED", "1.0"))

# ---------------------------------------------------------------- geometria
ANCHO_BUCKET = 1.4
Y_BUCKETS = 2.05
Y_ENTRADA0 = 1.3
DY_ENTRADA = 0.55
Y_LISTA = -1.5
DX_SLOT = 3.0

# ---------------------------------------------------------------- colores
C_NODO = BLUE_C
C_ENTRADA = TEAL
C_ENLACE = GRAY_B
C_ACTIVO = YELLOW
C_OK = GREEN
C_MAL = RED


def cargar_trace(ruta=RUTA_TRACE):
    """Lee el JSONL y lo agrupa por escenario: {nombre: {"init":..., "ops":[...]}}"""
    escenarios = {}
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            d = json.loads(linea)
            e = escenarios.setdefault(d["scenario"], {"init": None, "ops": []})
            if d["type"] == "init":
                e["init"] = d
            else:
                e["ops"].append(d)
    return escenarios


class VistaLRU(Scene):
    """Dibuja la tabla hash (arriba) y la lista doblemente enlazada (abajo) y
    anima cada evento del trace. Las escenas concretas heredan de esta clase."""

    # ------------------------------------------------------------ utilidades
    def rt(self, t):
        return t * VELOCIDAD

    def bx(self, b):
        return (b - (self.m - 1) / 2) * ANCHO_BUCKET

    def pos_bucket(self, b):
        return np.array([self.bx(b), Y_BUCKETS, 0])

    def pos_entrada(self, b, j):
        return np.array([self.bx(b), Y_ENTRADA0 - j * DY_ENTRADA, 0])

    def pos_nodo(self, slot):
        return np.array([(slot - (self.cap - 1) / 2) * DX_SLOT, Y_LISTA, 0])

    # ------------------------------------------------------------ mobjects
    def crear_nodo(self, k, v):
        caja = RoundedRectangle(corner_radius=0.12, width=2.0, height=1.0,
                                stroke_color=C_NODO, stroke_width=3,
                                fill_color="#0f2a33", fill_opacity=1)
        tk = Text(f"Key: {k}", font_size=22, color=YELLOW)
        tv = Text(f"Val: {v}", font_size=22)
        VGroup(tk, tv).arrange(DOWN, buff=0.1).move_to(caja)
        return VGroup(caja, tk, tv)

    def crear_entrada(self, k):
        caja = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.42,
                                stroke_color=C_ENTRADA, stroke_width=2.5,
                                fill_color="#0d2626", fill_opacity=1)
        return VGroup(caja, Text(str(k), font_size=20))

    def crear_texto_caption(self, texto, color=WHITE):
        t = Text(texto, font_size=26, color=color)
        if t.width > 12.5:
            t.scale_to_fit_width(12.5)
        return t.move_to([0, -3.4, 0])

    def crear_texto_tag(self, texto):
        t = Text(texto, font_size=18, color=GRAY_B)
        if t.width > 12.5:
            t.scale_to_fit_width(12.5)
        return t.move_to([0, -3.85, 0])

    def crear_titulo_op(self, texto):
        return Text(texto, font_size=38, color=YELLOW).move_to([0, 3.5, 0])

    # ------------------------------------------------------------ preparacion
    def preparar(self, init):
        """Dibuja lo estatico (buckets, ranuras, etiquetas) y reinicia el estado."""
        self.cap = init["capacity"]
        self.m = init["m"]
        self.nodos = {}      # clave -> VGroup del nodo de la lista
        self.entradas = {}   # clave -> VGroup de la entrada (HashNode) en su bucket
        self.orden = []      # [[k, v], ...] de head (MRU) a tail (LRU)
        self.cadenas = [[] for _ in range(self.m)]
        self.links = VGroup()
        self.links_visibles = False
        self.bucket_actual = 0

        self.buckets = VGroup(*[
            Rectangle(width=ANCHO_BUCKET - 0.2, height=0.55, stroke_color=GRAY_B,
                      stroke_width=2.5).move_to(self.pos_bucket(b))
            for b in range(self.m)
        ])
        indices = VGroup(*[
            Text(str(b), font_size=18, color=GRAY_B).move_to(self.pos_bucket(b) + UP * 0.5)
            for b in range(self.m)
        ])
        t_hash = Text(f"Tabla hash (m = {self.m}, encadenamiento)", font_size=20,
                      color=GRAY_B).move_to([0, 2.95, 0])
        ranuras = VGroup(*[
            Rectangle(width=2.3, height=1.2, stroke_color=GRAY, stroke_width=1.5,
                      stroke_opacity=0.5).move_to(self.pos_nodo(i))
            for i in range(self.cap)
        ])
        t_lista = Text(f"Lista doblemente enlazada (capacidad = {self.cap})",
                       font_size=20, color=GRAY_B).move_to([0, -2.85, 0])

        self.lbl_head = Text("MRU (Head)", font_size=20, color=C_OK)
        self.lbl_tail = Text("LRU (Tail)", font_size=20, color=C_MAL)
        self.lbl_ambos = Text("Head = Tail", font_size=20, color=C_ACTIVO)
        for lbl, (pos, op) in zip((self.lbl_head, self.lbl_tail, self.lbl_ambos),
                                  self.objetivos_etiquetas(0)):
            lbl.move_to(pos).set_opacity(op)

        self.titulo_op = self.crear_titulo_op("Estado inicial")
        self.caption = self.crear_texto_caption("Caché vacía", WHITE)
        self.tag = self.crear_texto_tag("trace.jsonl")

        self.add(self.buckets, indices, t_hash, ranuras, t_lista,
                 self.lbl_head, self.lbl_tail, self.lbl_ambos,
                 self.titulo_op, self.caption, self.tag)

    def objetivos_etiquetas(self, n):
        """[(posicion, opacidad)] para (head, tail, ambos) segun cuantos nodos hay."""
        abajo = DOWN * 0.95
        if n == 0:
            p = self.pos_nodo(0) + abajo
            return [(p, 0), (p, 0), (p, 0)]
        if n == 1:
            p = self.pos_nodo(0) + abajo
            return [(p, 0), (p, 0), (p, 1)]
        return [(self.pos_nodo(0) + abajo, 1), (self.pos_nodo(n - 1) + abajo, 1),
                (self.pos_nodo(0) + abajo, 0)]

    def anims_etiquetas(self, n):
        objs = self.objetivos_etiquetas(n)
        return [lbl.animate.move_to(pos).set_opacity(op)
                for lbl, (pos, op) in zip((self.lbl_head, self.lbl_tail, self.lbl_ambos), objs)]

    # ------------------------------------------------------------ enlaces
    def enlaces_lista(self, n):
        g = VGroup()
        for i in range(n - 1):
            a = self.pos_nodo(i) + RIGHT * 1.0
            b = self.pos_nodo(i + 1) + LEFT * 1.0
            g.add(DoubleArrow(a, b, buff=0.05, stroke_width=3, tip_length=0.18, color=C_ENLACE))
        return g

    def firma_enlaces(self, orden, cadenas):
        """Flechas prev/next de la lista + punteros de cada HashNode a su nodo."""
        g = self.enlaces_lista(len(orden))
        slot_de = {k: i for i, (k, _) in enumerate(orden)}
        for b, cadena in enumerate(cadenas):
            for j, k in enumerate(cadena):
                if k not in slot_de:
                    continue
                ent = self.pos_entrada(b, j)
                inicio = ent + (DOWN * 0.21 if j == len(cadena) - 1 else RIGHT * 0.45)
                fin = self.pos_nodo(slot_de[k]) + UP * 0.5
                g.add(Arrow(inicio, fin, buff=0.04, stroke_width=2.5, tip_length=0.15,
                            color=C_ENTRADA, max_tip_length_to_length_ratio=0.25))
        g.set_z_index(-1)
        return g

    # ------------------------------------------------------------ estado
    def cargar_estado(self, orden, cadenas):
        """Coloca un estado directamente, sin animar (para saltar al punto de interes)."""
        for slot, (k, v) in enumerate(orden):
            n = self.crear_nodo(k, v).move_to(self.pos_nodo(slot))
            self.nodos[k] = n
            self.add(n)
        for b, cad in enumerate(cadenas):
            for j, k in enumerate(cad):
                e = self.crear_entrada(k).move_to(self.pos_entrada(b, j))
                self.entradas[k] = e
                self.add(e)
        self.orden = [list(x) for x in orden]
        self.cadenas = [list(c) for c in cadenas]
        self.links = self.firma_enlaces(self.orden, self.cadenas)
        self.add(self.links)
        self.links_visibles = True
        for lbl, (pos, op) in zip((self.lbl_head, self.lbl_tail, self.lbl_ambos),
                                  self.objetivos_etiquetas(len(orden))):
            lbl.move_to(pos).set_opacity(op)

    def sincronizar(self, orden, cadenas, con_enlaces=True, dur=0.9):
        """Anima desde el estado dibujado hasta (orden, cadenas): crea, mueve y quita."""
        anims = []
        if self.links_visibles:
            anims.append(FadeOut(self.links))
            self.links_visibles = False

        claves = [k for k, _ in orden]
        for k in list(self.nodos):
            if k not in claves:
                anims.append(FadeOut(self.nodos.pop(k)))
        for slot, (k, v) in enumerate(orden):
            pos = self.pos_nodo(slot)
            if k in self.nodos:
                anims.append(self.nodos[k].animate.move_to(pos))
            else:
                n = self.crear_nodo(k, v).move_to(pos)
                self.nodos[k] = n
                anims.append(FadeIn(n, shift=DOWN * 0.6))

        en_hash = {k for cad in cadenas for k in cad}
        for k in list(self.entradas):
            if k not in en_hash:
                anims.append(FadeOut(self.entradas.pop(k)))
        for b, cad in enumerate(cadenas):
            for j, k in enumerate(cad):
                pos = self.pos_entrada(b, j)
                if k in self.entradas:
                    anims.append(self.entradas[k].animate.move_to(pos))
                else:
                    e = self.crear_entrada(k).move_to(pos)
                    self.entradas[k] = e
                    anims.append(FadeIn(e, shift=DOWN * 0.3))

        anims += self.anims_etiquetas(len(orden))
        self.play(*anims, run_time=self.rt(dur))
        self.orden = [list(x) for x in orden]
        self.cadenas = [list(c) for c in cadenas]

        if con_enlaces:
            self.links = self.firma_enlaces(self.orden, self.cadenas)
            self.play(FadeIn(self.links), run_time=self.rt(0.4))
            self.links_visibles = True

    # ------------------------------------------------------------ textos
    def narrar(self, caption=None, tag=None, color=WHITE, extra=(), dur=0.5):
        """Cambia el texto inferior (caption) y la linea del trace (tag), con animaciones extra."""
        anims = list(extra)
        if caption is not None:
            nuevo = self.crear_texto_caption(caption, color)
            anims.append(FadeTransform(self.caption, nuevo))
            self.caption = nuevo
        if tag is not None:
            nuevo_tag = self.crear_texto_tag(tag)
            anims.append(FadeTransform(self.tag, nuevo_tag))
            self.tag = nuevo_tag
        if anims:
            self.play(*anims, run_time=self.rt(dur))

    @staticmethod
    def texto_evento(paso):
        campos = " ".join(f"{k}={str(v).lower() if isinstance(v, bool) else v}"
                          for k, v in paso.items() if k != "e")
        return f"TRACE  {paso['e']} {campos}".strip()

    def cambiar_titulo(self, texto):
        nuevo = self.crear_titulo_op(texto)
        self.play(FadeTransform(self.titulo_op, nuevo), run_time=self.rt(0.4))
        self.titulo_op = nuevo

    # ------------------------------------------------------------ operaciones
    def ejecutar_op(self, op):
        if op["op"] == "put":
            self.cambiar_titulo(f"put({op['key']}, {op['value']})")
        else:
            self.cambiar_titulo(f"get({op['key']})")

        for paso in op["steps"]:
            self.animar_paso(paso, op)

        # Red de seguridad: lo dibujado debe coincidir con el estado real del trace.
        if self.orden != [list(x) for x in op["list"]] or self.cadenas != op["buckets"]:
            self.sincronizar(op["list"], op["buckets"])
        self.wait(self.rt(0.8))

    def animar_paso(self, s, op):
        e = s["e"]
        tag = self.texto_evento(s)
        clave = op["key"]

        if e == "HASH":
            self.bucket_actual = s["bucket"]
            self.narrar(f"bucket = {s['key']} % {self.m} = {s['bucket']}", tag, WHITE,
                        extra=[Indicate(self.buckets[s["bucket"]], color=C_ACTIVO, scale_factor=1.15)])

        elif e == "PROBE":
            ok = s["match"]
            txt = (f"Se recorre la cadena: clave {s['key']} == {clave}, encontrada" if ok
                   else f"Se recorre la cadena: clave {s['key']} != {clave}, se sigue")
            self.narrar(txt, tag, C_OK if ok else WHITE,
                        extra=[Indicate(self.entradas[s["key"]], color=C_OK if ok else C_MAL)])

        elif e == "HIT":
            self.narrar(f"Cache HIT: la tabla devuelve el puntero al nodo (valor = {op['result']})",
                        tag, C_OK, extra=[Indicate(self.nodos[s["key"]][0], color=C_OK)])

        elif e == "MISS":
            self.narrar("Cache MISS: la clave no está en la tabla, get devuelve -1", tag, C_MAL,
                        extra=[Indicate(self.buckets[self.bucket_actual], color=C_MAL)])
            self.wait(self.rt(0.6))

        elif e == "UPDATE":
            self.narrar(f"La clave ya existe: se actualiza su valor a {s['value']}", tag, C_ACTIVO)
            self.actualizar_valor(s["key"], s["value"])

        elif e == "ALREADY_HEAD":
            self.narrar("El nodo ya es la cabeza (MRU): no hay nada que mover", tag, C_ACTIVO,
                        extra=[Indicate(self.nodos[s["key"]][0], color=C_ACTIVO)])
            self.wait(self.rt(0.6))

        elif e == "MOVE_TO_FRONT":
            self.animar_mover(s, op, tag)

        elif e == "EVICT":
            k = s["key"]
            self.narrar(f"Caché llena: se expulsa la cola (LRU), clave {k}", tag, C_MAL)
            self.play(self.nodos[k][0].animate.set_stroke(C_MAL, width=6).set_fill("#3a1212"),
                      self.entradas[k][0].animate.set_stroke(C_MAL, width=5),
                      run_time=self.rt(0.5))
            self.wait(self.rt(0.4))
            orden = [x for x in self.orden if x[0] != k]
            cadenas = [[c for c in cad if c != k] for cad in self.cadenas]
            self.sincronizar(orden, cadenas, con_enlaces=False, dur=0.8)

        elif e == "INSERT":
            self.narrar(f"Se inserta la clave {s['key']}: bucket {s['bucket']} y cabeza de la lista",
                        tag, C_OK)
            self.sincronizar(op["list"], op["buckets"])
            self.play(Indicate(self.nodos[s["key"]][0], color=C_OK), run_time=self.rt(0.6))

    def actualizar_valor(self, k, v):
        vt = self.nodos[k][2]
        nuevo = Text(f"Val: {v}", font_size=22).move_to(vt)
        self.play(Transform(vt, nuevo), run_time=self.rt(0.6))
        for x in self.orden:
            if x[0] == k:
                x[1] = v

    def animar_mover(self, s, op, tag):
        """move_to_front en dos fases: desconectar y reconectar como cabeza."""
        k = s["key"]
        nodo = self.nodos[k]
        final = [list(x) for x in op["list"]]                 # k queda en la posicion 0
        sin_k = [x for x in self.orden if x[0] != k]

        self.narrar("move_to_front: el nodo pasa a ser el más reciente (MRU)", tag, C_ACTIVO,
                    extra=[nodo[0].animate.set_stroke(C_ACTIVO, width=6)])

        # Fase 1: desconectar
        if s["was_tail"]:
            self.narrar("1) Era la cola: tail = node->prev;  tail->next = nullptr", None, C_ACTIVO)
        else:
            self.narrar("1) Desconectar: prev->next = next;  next->prev = prev", None, C_ACTIVO)
        anims = [nodo.animate.shift(UP * 1.0)]
        if self.links_visibles:
            anims.append(FadeOut(self.links))
            self.links_visibles = False
        for slot, (kk, _) in enumerate(sin_k):
            anims.append(self.nodos[kk].animate.move_to(self.pos_nodo(slot)))
        self.play(*anims, run_time=self.rt(1.0))
        enl = self.enlaces_lista(len(sin_k))
        if len(enl) > 0:
            self.play(FadeIn(enl), run_time=self.rt(0.4))
        self.wait(self.rt(0.7))

        # Fase 2: reconectar como nueva cabeza
        self.narrar("2) Reconectar: node->next = head;  head->prev = node;  head = node",
                    None, C_ACTIVO)
        if len(enl) > 0:
            self.play(FadeOut(enl), run_time=self.rt(0.2))
        anims = [nodo.animate.move_to(self.pos_nodo(0))]
        for slot, (kk, _) in enumerate(final):
            if kk != k:
                anims.append(self.nodos[kk].animate.move_to(self.pos_nodo(slot)))
        self.play(*anims, run_time=self.rt(1.0))
        self.play(nodo[0].animate.set_stroke(C_NODO, width=3), run_time=self.rt(0.3))
        self.orden = final
        self.links = self.firma_enlaces(self.orden, self.cadenas)
        self.play(FadeIn(self.links), run_time=self.rt(0.4))
        self.links_visibles = True


# =====================================================================
#  ESCENAS (una por bloque del guion que sale del trace)
# =====================================================================
class Bloque05_06_Estructura(VistaLRU):
    """Componentes y unificacion: se cargan tres claves y se ve como la tabla
    apunta a los nodos de la lista."""

    def construct(self):
        esc = cargar_trace()["principal"]
        self.preparar(esc["init"])
        self.wait(1)
        self.narrar("Arriba: tabla hash con encadenamiento.  Abajo: lista doblemente enlazada",
                    "estado inicial: caché vacía", WHITE, dur=0.6)
        self.wait(2.5)
        for op in esc["ops"][:3]:
            self.ejecutar_op(op)
        self.narrar("Cada entrada de la tabla guarda la clave y un puntero al nodo de la lista",
                    "trace.jsonl", C_ENTRADA, extra=[Indicate(self.links, color=C_ENTRADA)], dur=1.2)
        self.wait(3)


class Bloque07_Punteros(VistaLRU):
    """move_to_front paso a paso sobre un nodo intermedio (get(2) con lista 3,2,1)."""

    def construct(self):
        esc = cargar_trace()["punteros"]
        self.preparar(esc["init"])
        ops = esc["ops"]
        listo = ops[2]                                 # estado tras put(1), put(2), put(3)
        self.cargar_estado(listo["list"], listo["buckets"])
        self.narrar("Estado de partida: lista 3, 2, 1 (ya insertadas)",
                    "estado del trace tras put(3, 30)", WHITE)
        self.wait(2)
        self.ejecutar_op(ops[3])                       # get(2)
        self.wait(3)


class Bloque09_Demostracion(VistaLRU):
    """Caso principal: put, put, put, get (hit), put con evicion, get (miss)."""

    def construct(self):
        esc = cargar_trace()["principal"]
        self.preparar(esc["init"])
        self.wait(1)
        for op in esc["ops"]:
            self.ejecutar_op(op)
        self.wait(2)


class Bloque10_CasosBorde(VistaLRU):
    """Cuatro casos borde, cada uno con su tarjeta de titulo."""

    CASOS = [
        # (escenario, titulo, cuantas operaciones se cargan sin animar)
        ("vacia", "Caso borde 1: get sobre una caché vacía", 0),
        ("capacidad1", "Caso borde 2: capacidad 1 (head = tail)", 0),
        ("actualizar", "Caso borde 3: put sobre una clave existente", 3),
        ("colision", "Caso borde 4: colisión en la tabla hash (1 % 7 == 8 % 7)", 0),
    ]

    def construct(self):
        trace = cargar_trace()
        for i, (nombre, titulo, precarga) in enumerate(self.CASOS):
            if i > 0:
                self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            tarjeta = Text(titulo, font_size=34, color=YELLOW)
            if tarjeta.width > 12.5:
                tarjeta.scale_to_fit_width(12.5)
            self.play(FadeIn(tarjeta), run_time=0.6)
            self.wait(1.4)
            self.play(FadeOut(tarjeta), run_time=0.4)

            esc = trace[nombre]
            self.preparar(esc["init"])
            ops = esc["ops"]
            if precarga:
                previo = ops[precarga - 1]
                self.cargar_estado(previo["list"], previo["buckets"])
                self.narrar("Estado de partida (ya insertadas)", "estado del trace", WHITE)
            self.wait(1)
            for op in ops[precarga:]:
                self.ejecutar_op(op)
            self.wait(1.5)
