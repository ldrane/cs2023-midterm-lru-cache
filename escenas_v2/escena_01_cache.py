"""
escenas_v2/escena_01_cache.py
Escena 1: Introducción conceptual a la Memoria Caché.
Duración calibrada: ~25 segundos para coincidir con la locución.
"""

from manim import *

# Paleta visual consistente con el proyecto
C_CPU = "#2A6F97"
C_CACHE = "#2A9D8F"       # Verde azulado / rápido
C_DISCO = "#E76F51"       # Rojo suave / lento y costoso
C_HIT = "#2EC4B6"
C_MISS = "#E63946"
C_TEXTO_SEC = "#A0AAB2"
C_RESALTE = "#F4A261"


class Escena01Cache(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO PRINCIPAL
        # -------------------------------------------------------------
        titulo = Text("¿Qué es una memoria caché?", font_size=42, color=YELLOW)
        titulo.to_edge(UP, buff=0.45)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.7)
        self.wait(0.5)

        # -------------------------------------------------------------
        # 2. BLOQUES DE ARQUITECTURA (CPU, Caché, Disco)
        # -------------------------------------------------------------
        # CPU a la izquierda
        caja_cpu = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.6,
                                    stroke_color=C_CPU, stroke_width=3,
                                    fill_color="#0d212d", fill_opacity=1)
        txt_cpu = Text("CPU / Servidor", font_size=23, color=WHITE).move_to(caja_cpu)
        cpu = VGroup(caja_cpu, txt_cpu).move_to([-4.8, -0.3, 0])

        # Caché arriba al centro (pequeña y rápida)
        caja_cache = RoundedRectangle(corner_radius=0.15, width=2.7, height=1.1,
                                      stroke_color=C_CACHE, stroke_width=3,
                                      fill_color="#0e2a27", fill_opacity=1)
        txt_cache = Text("Memoria Caché", font_size=21, color=WHITE).move_to(caja_cache)
        sub_cache = Text("ultrarrápida • capacidad fija N", font_size=15, color=C_CACHE)
        sub_cache.next_to(caja_cache, DOWN, buff=0.12)
        cache = VGroup(caja_cache, txt_cache, sub_cache).move_to([0.2, 1.6, 0])

        # Disco / Base de datos a la derecha (redimensionado para que todo quepa adentro)
        caja_disco = RoundedRectangle(corner_radius=0.15, width=3.9, height=2.3,
                                      stroke_color=C_DISCO, stroke_width=3,
                                      fill_color="#2b1411", fill_opacity=1)
        txt_disco = Text("Disco / Base de datos", font_size=20, color=WHITE)
        sub_disco = Text("capacidad masiva • latencia alta", font_size=15, color=C_DISCO)
        textos_disco = VGroup(txt_disco, sub_disco).arrange(DOWN, buff=0.18).move_to(caja_disco.get_center())
        disco = VGroup(caja_disco, textos_disco).move_to([4.8, -0.4, 0])

        # Texto explicativo inferior
        pie = Text("El acceso a almacenamiento persistente es lento; la caché minimiza esa espera.",
                   font_size=20, color=C_TEXTO_SEC).move_to([0, -3.3, 0])

        # Animación de aparición
        self.play(FadeIn(cpu, shift=RIGHT * 0.3), run_time=0.7)
        self.play(FadeIn(cache, shift=DOWN * 0.3), FadeIn(disco, shift=LEFT * 0.3), run_time=0.9)
        self.play(FadeIn(pie), run_time=0.6)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 3. CAMINO CORTO: CACHE HIT (Flecha doble + pulso ida y vuelta)
        # -------------------------------------------------------------
        pt_cpu_hit = caja_cpu.get_top() + RIGHT * 0.4
        pt_cache_hit = caja_cache.get_left() + DOWN * 0.15

        flecha_hit = DoubleArrow(pt_cpu_hit, pt_cache_hit, buff=0.12,
                                 stroke_width=4.5, color=C_HIT, tip_length=0.2)
        
        lbl_hit = VGroup(
            Text("Cache HIT", font_size=21, color=C_HIT, weight=BOLD),
            Text("Respuesta inmediata", font_size=17, color=WHITE)
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([-2.7, 2.05, 0])

        pulso_hit = Dot(point=pt_cpu_hit, radius=0.10, color=YELLOW)

        self.play(GrowFromPoint(flecha_hit, pt_cpu_hit), FadeIn(lbl_hit, shift=UP * 0.2), run_time=0.7)
        self.add(pulso_hit)
        # Ida rápida (CPU -> Caché)
        self.play(pulso_hit.animate.move_to(pt_cache_hit), run_time=0.35, rate_func=linear)
        self.play(Indicate(caja_cache, color=C_HIT, scale_factor=1.06), run_time=0.35)
        # Retorno rápido (Caché -> CPU)
        self.play(pulso_hit.animate.move_to(pt_cpu_hit), run_time=0.35, rate_func=linear)
        self.remove(pulso_hit)

        nuevo_pie_hit = Text("Cache HIT: El dato reside en la memoria rápida. Latencia casi nula.",
                             font_size=20, color=C_HIT).move_to([0, -3.3, 0])
        self.play(Transform(pie, nuevo_pie_hit), run_time=0.4)
        self.wait(3.5)

        # -------------------------------------------------------------
        # 4. CAMINO LARGO: CACHE MISS (Flecha doble + pulso lento)
        # -------------------------------------------------------------
        pt_cpu_miss = caja_cpu.get_right() + DOWN * 0.25
        pt_disco_miss = caja_disco.get_left() + DOWN * 0.1

        flecha_miss = DoubleArrow(pt_cpu_miss, pt_disco_miss, buff=0.15,
                                  stroke_width=4.5, color=C_MISS, tip_length=0.2)
        
        lbl_miss = VGroup(
            Text("Cache MISS", font_size=21, color=C_MISS, weight=BOLD),
            Text("Acceso costoso y lento", font_size=17, color=WHITE)
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([0.2, -0.9, 0])

        pulso_miss = Dot(point=pt_cpu_miss, radius=0.11, color=YELLOW)

        self.play(GrowFromPoint(flecha_miss, pt_cpu_miss), FadeIn(lbl_miss, shift=UP * 0.2), run_time=0.7)
        self.add(pulso_miss)
        # Ida lenta hacia el disco
        self.play(pulso_miss.animate.move_to(pt_disco_miss), run_time=1.4, rate_func=linear)
        self.play(Indicate(caja_disco, color=C_MISS, scale_factor=1.04), run_time=0.5)
        # Retorno lento al CPU
        self.play(pulso_miss.animate.move_to(pt_cpu_miss), run_time=1.4, rate_func=linear)
        self.remove(pulso_miss)

        nuevo_pie_miss = Text("Cache MISS: No está en caché. Se acude al disco y se paga alta latencia.",
                              font_size=20, color=C_MISS).move_to([0, -3.3, 0])
        self.play(Transform(pie, nuevo_pie_miss), run_time=0.4)
        self.wait(3.0)

        # -------------------------------------------------------------
        # 5. REMATE / TRANSICIÓN HACIA LRU
        # -------------------------------------------------------------
        nuevo_pie_final = Text("Como la caché es finita, necesitamos una política inteligente: LRU.",
                               font_size=22, color=C_RESALTE).move_to([0, -3.3, 0])
        self.play(Transform(pie, nuevo_pie_final), Circumscribe(caja_cache, color=C_RESALTE, time_width=0.8), run_time=1.0)
        self.wait(3.5)