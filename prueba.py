from manim import *

class LRUCacheAnimation(Scene):
    def construct(self):
        # 1. TÍTULO Y PANEL DE CONTROL SUPERIOR
        titulo = Text("LRU Cache - Simulación Visual", font_size=32, color=YELLOW)
        titulo.to_edge(UP)
        
        capacidad_txt = Text("Capacidad: 3", font_size=20, color=GRAY).next_to(titulo, DOWN, buff=0.2)
        estado_op = Text("Inicio: Caché vacía", font_size=22, color=WHITE).next_to(capacidad_txt, DOWN, buff=0.3)
        
        self.play(Write(titulo), FadeIn(capacidad_txt), Write(estado_op))
        self.wait(1)

        # Indicadores de extremos (MRU a la izquierda, LRU a la derecha)
        lbl_mru = Text("MRU (Head)", font_size=18, color=GREEN).shift(UP * 0.8 + LEFT * 3.5)
        lbl_lru = Text("LRU (Tail)", font_size=18, color=RED).shift(UP * 0.8 + RIGHT * 3.5)
        self.play(FadeIn(lbl_mru), FadeIn(lbl_lru))

        # Estructura para almacenar los VGroups de los nodos visuales
        nodos_visuales = []

        # Función auxiliar para construir el gráfico de un nodo
        def crear_nodo_mobj(key, val, color=BLUE):
            caja = RoundedRectangle(corner_radius=0.15, width=2.1, height=1.1, color=color, fill_opacity=0.2)
            k_txt = Text(f"Key: {key}", font_size=18, color=YELLOW).shift(UP * 0.2)
            v_txt = Text(f"Val: {val}", font_size=18, color=WHITE).shift(DOWN * 0.2)
            return VGroup(caja, k_txt, v_txt)

        # Función auxiliar para reposicionar y animar los nodos en pantalla
        def reposicionar_nodos():
            animaciones = []
            total = len(nodos_visuales)
            for i, n in enumerate(nodos_visuales):
                # Centrado horizontalmente con separación de 2.6 unidades
                x_pos = (i - (total - 1) / 2.0) * 2.6
                animaciones.append(n.animate.move_to(np.array([x_pos, -0.6, 0])))
            return animaciones

        # -------------------------------------------------------------
        # CASO 1: Llenar la caché con put(1, 10), put(2, 20), put(3, 30)
        # -------------------------------------------------------------
        datos_iniciales = [(1, 10), (2, 20), (3, 30)]
        for k, v in datos_iniciales:
            self.play(Transform(estado_op, Text(f"Operación: put({k}, {v}) -> Insertar en Head", font_size=22, color=BLUE)))
            nuevo_nodo = crear_nodo_mobj(k, v)
            nuevo_nodo.move_to(UP * 2 + LEFT * 4) # Aparece arriba a la izquierda
            
            nodos_visuales.insert(0, nuevo_nodo) # Va al inicio (Head/MRU)
            self.play(FadeIn(nuevo_nodo))
            self.play(*reposicionar_nodos(), run_time=0.8)
            self.wait(0.8)

        # -------------------------------------------------------------
        # CASO 2: Cache Hit con get(1) -> Debe moverse a Head (MRU)
        # -------------------------------------------------------------
        self.play(Transform(estado_op, Text("Operación: get(1) -> Cache Hit! Mover al frente", font_size=22, color=GREEN)))
        
        # En este momento el orden es [3, 2, 1]. El nodo 1 está en el índice 2
        nodo_hit = nodos_visuales[2]
        
        # Resaltar en amarillo que fue consultado
        self.play(nodo_hit[0].animate.set_color(YELLOW), run_time=0.4)
        
        # Reordenar en la lista visual (pasa al índice 0)
        nodos_visuales.remove(nodo_hit)
        nodos_visuales.insert(0, nodo_hit)
        
        # Animación de elevación y reubicación al frente
        self.play(nodo_hit.animate.shift(UP * 1.2), run_time=0.6)
        self.play(*reposicionar_nodos(), run_time=0.8)
        self.play(nodo_hit[0].animate.set_color(BLUE), run_time=0.4)
        self.wait(1)

        # -------------------------------------------------------------
        # CASO 3: Desalojo con put(4, 40) -> Caché llena, expulsa LRU
        # -------------------------------------------------------------
        # Ahora el orden es [1, 3, 2]. El nodo 2 es el LRU (Tail)
        self.play(Transform(estado_op, Text("Operación: put(4, 40) -> Caché Llena: Expulsar Tail (LRU: 2)", font_size=22, color=RED)))
        
        nodo_desalojado = nodos_visuales.pop() # Extrae el último elemento
        
        # Parpadeo en rojo para indicar expulsión
        self.play(nodo_desalojado[0].animate.set_color(RED), run_time=0.4)
        self.play(nodo_desalojado.animate.shift(DOWN * 1.5).fade(1), run_time=0.8)
        self.remove(nodo_desalojado)

        # Insertar el nuevo elemento 4 al frente
        nuevo_nodo_4 = crear_nodo_mobj(4, 40, color=BLUE)
        nuevo_nodo_4.move_to(UP * 2 + LEFT * 4)
        nodos_visuales.insert(0, nuevo_nodo_4)
        
        self.play(FadeIn(nuevo_nodo_4))
        self.play(*reposicionar_nodos(), run_time=0.8)
        
        self.play(Transform(estado_op, Text("Estado final: [4:40] -> [1:10] -> [3:30]", font_size=22, color=WHITE)))
        self.wait(2)