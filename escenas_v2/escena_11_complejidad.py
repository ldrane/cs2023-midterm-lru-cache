"""
escenas_v2/escena_11_complejidad.py
Escena 11: Análisis formal de Complejidad Big-O y Cierre del Proyecto.
Sincronizado a 47.5 s con señalamiento visual del Peor Caso y Caso Promedio.
"""

from manim import *

C_OK = GREEN
C_MAL = RED
C_ACTIVO = YELLOW
C_APAGADO = GRAY_B
C_NODO = BLUE_C


class Escena11Complejidad(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # 1. TÍTULO Y TABLA COMPLETA (0:00 - 0:04)
        # -------------------------------------------------------------
        titulo = Text("Evaluación de Complejidad Asintótica Big-O", font_size=36, color=YELLOW)
        titulo.to_edge(UP, buff=0.38)

        sub = Text("Análisis formal de costo temporal y espacial para capacidad fija K",
                   font_size=17, color=C_APAGADO).next_to(titulo, DOWN, buff=0.14)

        w_total = 11.2
        h_total = 2.85
        y_tabla = 0.40
        
        # Marco exterior curvo elegante
        marco_tabla = RoundedRectangle(
            corner_radius=0.18,
            width=w_total,
            height=h_total,
            stroke_color="#2b4162",
            stroke_width=2.5,
            fill_color="#091420",
            fill_opacity=0.92
        ).move_to([0, y_tabla, 0])

        cabecera_fondo = RoundedRectangle(
            corner_radius=0.18,
            width=w_total,
            height=0.58,
            stroke_color="#2b4162",
            stroke_width=1.5,
            fill_color="#142c47",
            fill_opacity=0.95
        ).move_to([0, y_tabla + h_total / 2 - 0.29, 0])

        w_cols = [2.9, 2.3, 3.8, 2.2]
        xs = [-4.15, -1.55, 1.50, 4.50]
        
        headers = ["Operación", "Caso Promedio", "Peor Caso (Colisión)", "Espacio"]
        txt_headers = VGroup(*[
            Text(headers[i], font_size=15, color=YELLOW, weight=BOLD).move_to([xs[i], y_tabla + h_total / 2 - 0.29, 0])
            for i in range(4)
        ])

        datos = [
            ("get(key)", "O(1)", "O(N) colisión hash", "O(1)"),
            ("put(key, value)", "O(1)", "O(N) rehashing/col.", "O(1)"),
            ("Desalojo (Evict)", "O(1) estricto", "O(1) estricto", "O(1)"),
            ("Memoria Global", "O(K) acotado", "O(K) acotado", "O(K)")
        ]

        lineas_h = VGroup()
        for r in range(4):
            y_l = (y_tabla + h_total / 2 - 0.58) - r * 0.56
            lineas_h.add(Line([-w_total / 2 + 0.1, y_l, 0], [w_total / 2 - 0.1, y_l, 0], color="#20334a", stroke_width=1.2))

        filas_mobjects = []
        for r_idx, fila in enumerate(datos):
            y_fila = (y_tabla + h_total / 2 - 0.58) - 0.28 - r_idx * 0.56
            es_memoria = (r_idx == 3)
            c_prom = C_OK if not es_memoria else C_ACTIVO
            c_peor = C_ACTIVO if r_idx < 2 else (C_OK if r_idx == 2 else C_ACTIVO)
            colores = [WHITE, c_prom, c_peor, C_OK]

            celdas = []
            for c_idx in range(4):
                t = Text(fila[c_idx], font_size=15, color=colores[c_idx], weight=BOLD if c_idx > 0 else NORMAL)
                t.move_to([xs[c_idx], y_fila, 0])
                celdas.append(t)
            filas_mobjects.append(VGroup(*celdas))

        tabla_completa = VGroup(marco_tabla, cabecera_fondo, txt_headers, lineas_h, *filas_mobjects)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), FadeIn(sub), run_time=0.8)
        self.play(FadeIn(tabla_completa), run_time=1.0)
        self.wait(2.2)  # Acumulado: 4.0s

        # -------------------------------------------------------------
        # 2. SEÑALIZACIÓN: COLUMNA "PEOR CASO (COLISIÓN)" (0:04 - 0:17 | 13.0 s)
        # Resalta en rojo/coral las celdas de colisión O(N)
        # -------------------------------------------------------------
        pildora_peor = RoundedRectangle(
            corner_radius=0.12,
            width=w_cols[2] + 0.1,
            height=1.20,
            stroke_color="#ff595e",
            stroke_width=2.5,
            fill_color="#ff595e",
            fill_opacity=0.14
        ).move_to([xs[2], y_tabla + 0.25, 0])

        self.play(FadeIn(pildora_peor), run_time=0.6)
        self.wait(11.8)
        self.play(FadeOut(pildora_peor), run_time=0.6)  # Acumulado: 17.0s

        # -------------------------------------------------------------
        # 3. RESALTE: COLUMNA "CASO PROMEDIO" (0:17 - 0:27 | 10.0 s)
        # Resalta en verde brillante las operaciones O(1)
        # -------------------------------------------------------------
        pildora_promedio = RoundedRectangle(
            corner_radius=0.12,
            width=w_cols[1] + 0.1,
            height=1.70,
            stroke_color=C_OK,
            stroke_width=2.6,
            fill_color=C_OK,
            fill_opacity=0.14
        ).move_to([xs[1], y_tabla - 0.02, 0])

        self.play(FadeIn(pildora_promedio), run_time=0.6)
        self.wait(8.8)
        self.play(FadeOut(pildora_promedio), run_time=0.6)  # Acumulado: 27.0s

        # -------------------------------------------------------------
        # 4. RECUADRO CONCLUSIÓN DEL DISEÑO (0:27 - 0:47.5 | 20.5 s)
        # -------------------------------------------------------------
        caja_concl = RoundedRectangle(
            corner_radius=0.16, width=w_total, height=1.38,
            stroke_color=YELLOW, stroke_width=2.6,
            fill_color="#0a1926", fill_opacity=0.98
        ).move_to([0, -2.15, 0])

        tit_c = Text("Conclusión del Diseño:", font_size=17, color=YELLOW, weight=BOLD)
        l1 = Text("• La dupla Hash Table + Doubly Linked List desacopla el orden temporal del acceso.", font_size=14, color=WHITE)
        l2 = Text("• Latencia O(1) promedio y determinista: el estándar en bases de datos y servidores web.", font_size=14, color=WHITE)

        txt_concl = VGroup(tit_c, l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        txt_concl.move_to(caja_concl.get_center()).align_to(caja_concl, LEFT).shift(RIGHT * 0.40)

        panel_final = VGroup(caja_concl, txt_concl)

        self.play(
            tabla_completa.animate.set_opacity(0.32),
            FadeIn(panel_final, shift=UP * 0.25),
            run_time=0.8
        )
        self.play(
            Indicate(caja_concl, color=C_ACTIVO, scale_factor=1.015),
            run_time=0.6
        )

        self.wait(19.1)  # Acumulado: 47.5s exactos