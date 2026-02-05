

from manim import *
import numpy as np


class ClasificacionDefensa(Scene):
    def construct(self):
        # --- CONFIGURACIÓN DE ESTILO ---
        self.camera.background_color = "#1a1a1a"  # Fondo oscuro tipo militar/radar

        # ---------------------------------------------------------
        # ESCENA 1: INTRODUCCIÓN
        # ---------------------------------------------------------
        self.add_sound("audio/Datos_escena2.wav")
        titulo = Text("CLASIFICACION: DEFENSA PLANETARIA", font_size=40, weight=BOLD, color=GREEN)
        subtitulo = Text("Clasificación Binaria: ¿Pájaro o Misil?", font_size=24, color=WHITE).next_to(titulo, DOWN)
        grupo = Text("Grupo 4: Carlos Angel, Jean Terrazo", font_size=20, color=GRAY).to_edge(DOWN)

        self.play(Write(titulo), FadeIn(subtitulo))
        self.play(FadeIn(grupo))
        self.wait(2)
        self.play(FadeOut(titulo), FadeOut(subtitulo), FadeOut(grupo))

        # ---------------------------------------------------------
        # ESCENA 2: EL RADAR MEJORADO CON TEXTO LATEX
        # ---------------------------------------------------------

        # Título de la escena
        escena_radar = Tex(
            "Sistema de Detección por Radar",
            font_size=36,
            color=GREEN_A
        ).to_edge(UP, buff=0.5)
        self.play(Write(escena_radar))

        # Crear interfaz de radar con más detalle
        radar_circle_outer = Circle(radius=3, color=GREEN_E, stroke_width=2)
        radar_circle_inner = Circle(radius=2, color=GREEN_E, stroke_width=1, stroke_opacity=0.5)
        radar_circle_mid = Circle(radius=1, color=GREEN_E, stroke_width=1, stroke_opacity=0.3)

        # Marcas de distancia (usando Text en lugar de Tex para evitar problemas)
        for r in [1, 2, 3]:
            distance_mark = Text(
                f"{r * 100} km",
                font_size=14,
                color=GREEN_E
            ).next_to(radar_circle_outer.point_at_angle(0), RIGHT, buff=0.1)
            distance_mark.shift(RIGHT * r * 0.3)


        # Líneas del radar con más ángulos
        radar_lines = VGroup()
        angles = [0, PI / 4, PI / 2, 3 * PI / 4, PI, 5 * PI / 4, 3 * PI / 2, 7 * PI / 4]
        angle_labels = ["0°", "45°", "90°", "135°", "180°", "225°", "270°", "315°"]

        for i, (angle, label_text) in enumerate(zip(angles, angle_labels)):
            line = Line(
                np.array([0, 0, 0]),
                np.array([3 * np.cos(angle), 3 * np.sin(angle), 0]),
                color=GREEN_E,
                stroke_width=1.5,
                stroke_opacity=0.7
            )
            radar_lines.add(line)

            # Etiquetas de ángulo usando Text
            label = Text(
                label_text,
                font_size=12,
                color=GREEN_E
            )
            label.move_to(np.array([3.3 * np.cos(angle), 3.3 * np.sin(angle), 0]))
            radar_lines.add(label)

        # Escáner con efecto de brillo
        radar_scanner = Line(
            ORIGIN,
            UP * 3,
            color=GREEN_A,
            stroke_width=6
        ).set_opacity(0.8)

        # Agregar efecto de brillo al escáner
        scanner_glow = Line(
            ORIGIN,
            UP * 3,
            color=GREEN_A,
            stroke_width=10
        ).set_opacity(0.3).add_updater(lambda m: m.move_to(radar_scanner))

        # Crear el radar completo
        radar = VGroup(radar_circle_outer, radar_circle_inner, radar_circle_mid, radar_lines)

        # Animación de aparición del radar
        self.play(
            Create(radar_circle_outer),
            Create(radar_circle_inner, run_time=1.5),
            Create(radar_circle_mid, run_time=1.2),
            Create(radar_lines, run_time=2),
            rate_func=smooth
        )

        # Añadir el escáner y su brillo
        self.add(scanner_glow)
        self.play(FadeIn(radar_scanner))

        # Leyenda del radar
        leyenda = VGroup(
            Text("Pájaro", color=GREEN, font_size=18),
            Text("Misil", color=RED, font_size=18)
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)

        for item in leyenda:
            circle = Circle(radius=0.15, color=item.get_color(), stroke_width=2)
            circle.next_to(item, LEFT, buff=0.2)
            leyenda.add(circle)

        self.play(FadeIn(leyenda, shift=UP * 0.5))

        # ---------------------------------------------------------
        # PUNTOS APARECIENDO UNO POR UNO
        # ---------------------------------------------------------
        np.random.seed(42)

        # Generar posiciones más realistas para radar
        birds_coords = []
        for _ in range(15):
            angle = np.random.uniform(0, 2 * PI)
            radius = np.random.uniform(0.5, 2.8)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            birds_coords.append([x, y, 0])

        missiles_coords = []
        for _ in range(8):
            angle = np.random.uniform(PI / 3, 2 * PI / 3)
            radius = np.random.uniform(1.0, 2.5)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            missiles_coords.append([x, y, 0])

        # Crear grupos vacíos
        birds_dots = VGroup()
        missiles_dots = VGroup()

        # Contador de objetos detectados
        counter_text = Text(
            "Objetos detectados: 0",
            font_size=20,
            color=YELLOW
        ).to_edge(UP + RIGHT, buff=0.5)
        self.play(Write(counter_text))

        # Animación secuencial de aparición
        total_objects = len(birds_coords) + len(missiles_coords)
        detected_count = 0

        # Primero aparecen 3 pájaros normales
        for i in range(3):
            dot = Dot(birds_coords[i], color=GREEN, radius=0.08)
            birds_dots.add(dot)
            detected_count += 1

            # Actualizar contador
            new_counter = Text(
                f"Objetos detectados: {detected_count}",
                font_size=20,
                color=YELLOW
            ).to_edge(UP + RIGHT, buff=0.5)

            self.play(
                FadeIn(dot, scale=0.5),
                Transform(counter_text, new_counter),
                run_time=0.3
            )
            self.wait(0.1)

        # Luego el primer misil
        dot = Dot(missiles_coords[0], color=RED, radius=0.12)
        missiles_dots.add(dot)
        detected_count += 1

        new_counter = Text(
            f"Objetos detectados: {detected_count}",
            font_size=20,
            color=YELLOW
        ).to_edge(UP + RIGHT, buff=0.5)

        self.play(
            Flash(dot, color=RED, line_length=0.3, flash_radius=0.4),
            FadeIn(dot, scale=0.3),
            Transform(counter_text, new_counter),
            run_time=0.5
        )

        # Texto de alerta cuando aparece el primer misil
        alert_text = Text(
            "¡ALERTA! Objeto de alta velocidad detectado",
            color=RED,
            font_size=28
        ).to_edge(UP, buff=2)
        self.play(Write(alert_text, run_time=0.8))
        self.play(FadeOut(alert_text, run_time=0.5))

        # Continuar alternando pájaros y misiles
        bird_idx = 3
        missile_idx = 1

        for count in range(total_objects - 4):
            if (count % 3 != 0) and (bird_idx < len(birds_coords)):
                dot = Dot(birds_coords[bird_idx], color=GREEN, radius=0.08)
                birds_dots.add(dot)
                detected_count += 1
                bird_idx += 1
                anim_time = 0.2
            elif missile_idx < len(missiles_coords):
                dot = Dot(missiles_coords[missile_idx], color=RED, radius=0.12)
                missiles_dots.add(dot)
                detected_count += 1
                missile_idx += 1
                anim_time = 0.4
            else:
                if bird_idx < len(birds_coords):
                    dot = Dot(birds_coords[bird_idx], color=GREEN, radius=0.08)
                    birds_dots.add(dot)
                    detected_count += 1
                    bird_idx += 1
                    anim_time = 0.2

            new_counter = Text(
                f"Objetos detectados: {detected_count}",
                font_size=20,
                color=YELLOW
            ).to_edge(UP + RIGHT, buff=0.5)

            if missile_idx > 1 and dot.get_color() == RED:
                self.play(
                    Flash(dot, color=RED, line_length=0.2, flash_radius=0.3),
                    FadeIn(dot, scale=0.3),
                    Transform(counter_text, new_counter),
                    run_time=anim_time
                )
            else:
                self.play(
                    FadeIn(dot, scale=0.5),
                    Transform(counter_text, new_counter),
                    run_time=anim_time
                )

            self.wait(0.05)

        # Texto final del radar
        final_count = Text(
            f"Total: {len(birds_dots)} pájaros, {len(missiles_dots)} misiles",
            font_size=22,
            color=YELLOW
        ).next_to(counter_text, DOWN, buff=0.3)

        self.play(Write(final_count))

        # ---------------------------------------------------------
        # ANIMACIÓN DEL RADAR ESCANEANDO
        # ---------------------------------------------------------
        self.play(
            Rotate(
                radar_scanner,
                angle=2 * PI,
                about_point=ORIGIN,
                run_time=4,
                rate_func=linear
            ),
            Rotate(
                scanner_glow,
                angle=2 * PI,
                about_point=ORIGIN,
                run_time=4,
                rate_func=linear
            )
        )

        # ---------------------------------------------------------
        # DESTELLOS EN LOS MISILES (ORDEN ESPECÍFICO)
        # ---------------------------------------------------------
        missiles_centers = [dot.get_center() for dot in missiles_dots]
        distances = [np.linalg.norm(center) for center in missiles_centers]
        sorted_indices = np.argsort(distances)

        # Etiqueta para los destellos
        flash_label = Text(
            "Análisis de amenazas en curso...",
            font_size=24,
            color=ORANGE
        ).to_edge(DOWN, buff=1)
        self.play(Write(flash_label))

        # Destellar cada misil en orden
        for idx in sorted_indices:
            misil = missiles_dots[idx]

            # Destello con ecuación de amenaza (usando Text simple)
            threat_level = f"{(1 - distances[idx] / 3):.2f}"
            threat_text = Text(
                f"Amenaza: {threat_level}",
                font_size=16,
                color=RED
            ).next_to(misil, UP, buff=0.2)

            self.play(
                Flash(
                    misil,
                    color=RED,
                    line_length=0.4,
                    num_lines=12,
                    flash_radius=0.6,
                    run_time=0.5
                ),
                Write(threat_text),
                rate_func=there_and_back_with_pause
            )

            self.play(FadeOut(threat_text))
            self.wait(0.1)

        self.play(FadeOut(flash_label))

        # Texto de transición
        trans_text = Text(
            "¡Problema de clasificación identificado!",
            font_size=30,
            color=YELLOW,
            weight=BOLD
        ).to_edge(DOWN, buff=0.5)



        # ---------------------------------------------------------
        # TRANSICIÓN A LA SIGUIENTE ESCENA
        # ---------------------------------------------------------
        self.play(
            FadeOut(trans_text),
            FadeOut(escena_radar),
            FadeOut(leyenda),
            FadeOut(counter_text),
            FadeOut(final_count),
            FadeOut(radar_circle_outer),
            FadeOut(radar_circle_inner),
            FadeOut(radar_circle_mid),
            FadeOut(radar_lines),
            FadeOut(radar_scanner, radar_lines, radar, scanner_glow)
        )
        scanner_glow.clear_updaters()
        # SEGUNDO: Agrupar todos los elementos del radar y eliminarlos juntos
        todo_el_radar = VGroup(
            radar_circle_outer,
            radar_circle_inner,
            radar_circle_mid,
            radar_lines,
            radar_scanner,
            scanner_glow,
            birds_dots,
            missiles_dots
        )

        self.play(
            todo_el_radar.animate.scale(0.5).set_opacity(0),
            run_time=1
        )

        # TERCERO: Remover explícitamente de la escena
        self.remove(*todo_el_radar)


        # ---------------------------------------------------------
        # ESCENA 3: LOS DATOS (FEATURE SPACE)
        # ---------------------------------------------------------
        # Transformar a plano cartesiano

        axes = Axes(
            x_range=[0, 1000, 200],  # Velocidad
            y_range=[0, 20, 5],  # Tamaño
            x_length=6, y_length=4.5,
            axis_config={"color": BLUE, "include_numbers": False},
        ).add_coordinates().to_edge(LEFT).shift(DOWN * 0.3)

        # Etiquetas de ejes
        x_label = axes.get_x_axis_label("Velocidad (km/h)").scale(0.6)
        y_label = axes.get_y_axis_label("Tamanio (m)").scale(0.6).rotate(90 * DEGREES)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Mover puntos a sus posiciones lógicas en el gráfico
        # Pájaros: Lentos (<300), Pequeños (<2m)
        new_birds_coords = []
        for _ in range(15):
            x = np.random.normal(200, 50)  # Lento
            y = np.random.normal(2, 1)  # Pequeño
            new_birds_coords.append(axes.c2p(x, y))

        # Misiles: Rápidos (>800), Pequeños (<3m)
        new_missiles_coords = []
        for _ in range(10):
            x = np.random.normal(900, 50)  # Muy rápido
            y = np.random.normal(3, 1)  # Pequeño
            new_missiles_coords.append(axes.c2p(x, y))

        # Aviones (Ruido): Rápidos, Grandes (>15m) - Opcional para la historia
        # Drones (Zona Confusa): Velocidad media, pequeño
        confused_coords = []
        for _ in range(5):
            x = np.random.normal(600, 100)  # Zona media
            y = np.random.normal(4, 2)
            confused_coords.append(axes.c2p(x, y))

        # Agrupar puntos nuevos
        final_birds = VGroup(*[Dot(p, color=GREEN) for p in new_birds_coords])
        final_missiles = VGroup(*[Dot(p, color=RED) for p in new_missiles_coords])
        final_confused = VGroup(*[Dot(p, color=YELLOW) for p in confused_coords])  # Zona amarilla

        # Transición visual: Puntos del radar -> Puntos del gráfico
        self.play(
            ReplacementTransform(birds_dots, final_birds),
            ReplacementTransform(missiles_dots, final_missiles),
            FadeIn(final_confused)
        )

        # Resaltar zona de confusión
        conf_circle = Circle(color=YELLOW).surround(final_confused)
        conf_text = Text("Zona de Confusión", font_size=20, color=YELLOW).next_to(conf_circle, UP)
        self.play(Create(conf_circle), Write(conf_text))

        self.wait(5)
        self.play(FadeOut(conf_circle), FadeOut(conf_text))

        # ---------------------------------------------------------
        # ESCENA 4: KNN (EL VECINO)
        # ---------------------------------------------------------

        self.add_sound("audio/KNN.wav")
        header_knn = Text("1.K-Nearest Neighbors (KNN)", font_size=28, color=TEAL_A).to_edge(UP)
        self.play(Write(header_knn))
        self.wait(5)

        # Punto desconocido (Gris)
        unknown_pos = axes.c2p(750, 3)  # Cerca de misiles pero en el borde
        unknown_dot = Dot(unknown_pos, color=GRAY, radius=0.12)
        lbl_unk = Text("¿?", font_size=20).next_to(unknown_dot, UP)

        self.play(FadeIn(unknown_dot), Write(lbl_unk))

        # Radio de búsqueda
        search_circle = Circle(radius=1.5, color=WHITE, stroke_opacity=0.5).move_to(unknown_pos)
        self.play(Create(search_circle))
        self.wait(8)

        # Líneas a vecinos (simulado)
        lines = VGroup()
        for dot in final_missiles:
            if np.linalg.norm(dot.get_center() - unknown_pos) < 1.5:
                lines.add(Line(unknown_pos, dot.get_center(), color=WHITE, stroke_width=1))

        self.play(Create(lines))
        self.wait(12)

        # Clasificación
        self.play(
            unknown_dot.animate.set_color(RED),  # Se vuelve misil
            Transform(lbl_unk, Text("¡MISIL!", color=RED, font_size=20).next_to(unknown_dot, UP))
        )
        self.wait(8)

        # Limpieza KNN
        self.play(FadeOut(header_knn), FadeOut(search_circle), FadeOut(lines), FadeOut(unknown_dot), FadeOut(lbl_unk))

        # ---------------------------------------------------------
        # ESCENA 5: ÁRBOLES DE DECISIÓN
        # ---------------------------------------------------------

        self.add_sound("audio/arbolesde.wav")
        header_tree = Text("2. Árboles de Decisión", font_size=28, color=ORANGE).to_edge(UP)
        self.play(Write(header_tree))
        self.wait(5)

        # Cortes en el plano
        # Corte 1: Velocidad > 500
        line_v = DashedLine(axes.c2p(500, 0), axes.c2p(500, 20), color=ORANGE)
        txt_v = Text("Vel > 500?", font_size=18, color=ORANGE).next_to(line_v, UP)

        self.play(Create(line_v), Write(txt_v))
        self.wait(8)

        # Sombrear zona izquierda (Pájaros)
        rect_birds = Rectangle(width=3, height=4.5, color=GREEN, fill_opacity=0.4, stroke_width=0).move_to(
            axes.c2p(250, 10))
        self.play(FadeIn(rect_birds))
        self.wait(5)

        # Corte 2: Tamaño < 5
        line_h = DashedLine(axes.c2p(500, 5), axes.c2p(1000, 5), color=ORANGE)
        txt_h = Text("Tam < 5?", font_size=18, color=ORANGE).next_to(line_h, RIGHT)

        self.play(Create(line_h), Write(txt_h))
        self.wait(10)

        # Sombrear zona misiles
        rect_missiles = Rectangle(width=3, height=1.5, color=RED, fill_opacity=0.2, stroke_width=0).align_to(line_v,
                                                                                                             LEFT).align_to(
            line_h, UP)
        # Ajuste manual de posición del rectangulo rojo para que coincida visualmente con la zona de misiles
        rect_missiles.move_to(axes.c2p(750, 2.5))

        self.play(FadeIn(rect_missiles))
        self.wait(6)

        # Limpieza Árboles
        self.play(
            FadeOut(header_tree), FadeOut(line_v), FadeOut(txt_v), FadeOut(line_h), FadeOut(txt_h),
            FadeOut(rect_birds), FadeOut(rect_missiles)
        )

        # ---------------------------------------------------------
        # ESCENA 6: REGRESIÓN LOGÍSTICA
        # ---------------------------------------------------------

        self.add_sound("audio/regresionlog.wav")
        header_log = Text("3. Regresión Logística (Probabilidad)", font_size=28, color=BLUE).to_edge(UP)
        self.play(Write(header_log))
        self.wait(6)

        # Frontera suave (Sigmoide)
        # Dibujamos una curva sutil entre los grupos
        sigmoid_curve = axes.plot(lambda x: 15 / (1 + np.exp(0.01 * (x - 600))), color=BLUE)
        self.play(Create(sigmoid_curve), run_time = 9)


        # Mostrar probabilidades
        p1 = Text("99% Misil", font_size=16, color=RED).move_to(axes.c2p(900, 2))
        p2 = Text("1% Misil", font_size=16, color=GREEN).move_to(axes.c2p(200, 2))
        p3 = Text("50%", font_size=16, color=YELLOW).move_to(axes.c2p(600, 8))

        self.play(Write(p1), Write(p2))
        self.wait(4)
        self.play(Write(p3))
        self.wait(4)

        # Limpieza final de gráfico
        self.play(
            FadeOut(header_log), FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(final_birds), FadeOut(final_missiles), FadeOut(final_confused),
            FadeOut(sigmoid_curve), FadeOut(p1), FadeOut(p2), FadeOut(p3)
        )

        # ---------------------------------------------------------
        # ESCENA 7: MATRIZ DE CONFUSIÓN Y CIERRE
        # ---------------------------------------------------------

        header_metrics = Text("Métricas de Evaluación", font_size=32).to_edge(UP)
        self.add_sound("audio/FIN.wav")
        # Tabla Matriz de Confusión
        # Usamos MobjectTable para control total
        t00 = Text("TP (Derribado)", color=GREEN, font_size=24)  # Correcto (Misil como Misil)
        t01 = Text("FN (Peligro!)", color=RED, font_size=24)  # Error (Misil como Pájaro)
        t10 = Text("FP (Error)", color=YELLOW, font_size=24)  # Error (Pájaro como Misil)
        t11 = Text("TN (Seguro)", color=GREEN, font_size=24)  # Correcto (Pájaro como Pájaro)

        matrix = MobjectTable(
            [[t00, t01], [t10, t11]],
            row_labels=[Text("Es Misil", font_size=20), Text("Es Pájaro", font_size=20)],
            col_labels=[Text("Dice Misil", font_size=20), Text("Dice Pájaro", font_size=20)],
            include_outer_lines=True
        ).scale(0.8)

        self.play(Write(header_metrics), Create(matrix), run_time=3)
        self.wait(5)
        # Resaltar errores y aciertos
        self.play(Indicate(t00, color=GREEN, scale_factor=1.2), run_time=2)  # TP
        self.play(Indicate(t10, color=YELLOW, scale_factor=1.2), run_time=2)  # FP (Pobre pájaro)
        self.wait(8)

        # Conclusión
        self.play(FadeOut(matrix), FadeOut(header_metrics))

        final_stats = VGroup(
            Text("Accuracy: 95%", color=GREEN, font_size=40),
            Text("F1-Score: 0.92", color=BLUE, font_size=40)
        ).arrange(DOWN, buff=0.5)

        final_msg = Text("Esto es Clasificación Binaria.", font_size=32, weight=BOLD).next_to(final_stats, DOWN, buff=1)

        self.play(Write(final_stats), run_time=2)
        self.wait(3)
        self.play(Write(final_msg))
        self.wait(5)

        credits = Text("Gracias.", font_size=24, color=GRAY).to_edge(DOWN)
        self.play(FadeIn(credits))
        self.wait(2)