"""
escenas_v2/escena_11_complejidad.py
Escena 11: Análisis formal de Complejidad Big-O y Cierre del Proyecto.
Tabla con bordes redondeados orgánicos y distribución simétrica limpia.
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
        # 1. TÍTULO SUPERIOR CENTRADO (0:00 - 0:06)
        # -------------------------------------------------------------
        titulo = Text("Evaluación de Complejidad Asintótica Big-O", font_size=36, color=YELLOW)
        titulo.to_edge(UP, buff=0.38)
        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)

        sub = Text("Análisis formal de costo temporal y espacial para capacidad fija K",
                   font_size=17, color=C_APAGADO).next_to(titulo, DOWN, buff=0.14)
        self.play(FadeIn(sub), run_time=0.5)

        # -------------------------------------------------------------
        # 2. TABLA CON BORDE REDONDEADO INTERIOR (0:06 - 0:18)
        # -------------------------------------------------------------
        w_total = 11.2
        h_total = 2.85
        y_tabla = 0.35
        
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

        # Banda del encabezado redondeada en la parte superior
        cabecera_fondo = RoundedRectangle(
            corner_radius=0.18,
            width=w_total,
            height=0.58,
            stroke_color="#2b4162",
            stroke_width=1.5,
            fill_color="#142c47",
            fill_opacity=0.95
        ).move_to([0, y_tabla + h_total / 2 - 0.29, 0])

        self.play(FadeIn(marco_tabla), FadeIn(cabecera_fondo), run_time=0.6)

        # Coordenadas y anchos de columnas
        w_cols = [2.9, 2.3, 3.8, 2.2]
        xs = [-4.15, -1.55, 1.50, 4.50]
        
        # Textos de encabezados
        headers = ["Operación", "Caso Promedio", "Peor Caso (Colisión)", "Espacio"]
        txt_headers = VGroup(*[
            Text(headers[i], font_size=15, color=YELLOW, weight=BOLD).move_to([xs[i], y_tabla + h_total / 2 - 0.29, 0])
            for i in range(4)
        ])
        self.play(FadeIn(txt_headers), run_time=0.5)

        # Filas de datos
        datos = [
            ("get(key)", "O(1)", "O(N) colisión hash", "O(1)"),
            ("put(key, value)", "O(1)", "O(N) rehashing/col.", "O(1)"),
            ("Desalojo (Evict)", "O(1) estricto", "O(1) estricto", "O(1)"),
            ("Memoria Global", "O(K) acotado", "O(K) acotado", "O(K)")
        ]

        # Líneas divisorias horizontales internas
        lineas_h = VGroup()
        for r in range(4):
            y_l = (y_tabla + h_total / 2 - 0.58) - r * 0.56
            lineas_h.add(Line([-w_total / 2 + 0.1, y_l, 0], [w_total / 2 - 0.1, y_l, 0], color="#20334a", stroke_width=1.2))

        self.play(Create(lineas_h), run_time=0.4)

        # Textos de las celdas
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

        self.play(
            LaggedStart(*[FadeIn(f, shift=DOWN * 0.1) for f in filas_mobjects], lag_ratio=0.2),
            run_time=1.2
        )
        self.wait(2.5)

        # -------------------------------------------------------------
        # RESALTADOR INTERIOR REDONDEADO (Calza exactamente en las operaciones O(1))
        # -------------------------------------------------------------
        # Cubre solo las filas 0, 1 y 2 (las operaciones en tiempo O(1)), sin pisar memoria
        pildora_resaltado = RoundedRectangle(
            corner_radius=0.12,
            width=w_cols[1] + 0.1,
            height=1.70,
            stroke_color=C_OK,
            stroke_width=2.5,
            fill_color=C_OK,
            fill_opacity=0.12
        ).move_to([xs[1], y_tabla - 0.02, 0])

        self.play(FadeIn(pildora_resaltado), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(pildora_resaltado), run_time=0.4)

        # -------------------------------------------------------------
        # 3. CONCLUSIÓN CENTRADA (11.2 unidades exactas) (0:18 - 0:31)
        # -------------------------------------------------------------
        caja_concl = RoundedRectangle(
            corner_radius=0.15, width=w_total, height=1.30,
            stroke_color=C_ACTIVO, stroke_width=2,
            fill_color="#0a1520", fill_opacity=0.95
        ).move_to([0, -2.2, 0])

        tit_c = Text("Conclusión del Diseño:", font_size=16, color=YELLOW, weight=BOLD)
        l1 = Text("• La dupla Hash Table + Doubly Linked List desacopla el orden temporal del acceso.", font_size=14, color=WHITE)
        l2 = Text("• Latencia O(1) constante y determinista: el estándar en bases de datos y servidores web.", font_size=14, color=WHITE)

        txt_concl = VGroup(tit_c, l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        txt_concl.move_to(caja_concl.get_center()).align_to(caja_concl, LEFT).shift(RIGHT * 0.35)

        panel_final = VGroup(caja_concl, txt_concl)
        self.play(FadeIn(panel_final, shift=UP * 0.2), run_time=0.7)
        self.wait(4.5)