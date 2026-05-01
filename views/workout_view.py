import flet as ft
import db_manager as db
import time
import threading
from models import User, Exercise
from supabase import Client
from datetime import datetime

def workout_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de entrenamiento avanzada con persistencia, series y cronómetro."""
    
    # --- ESTADO Y PERSISTENCIA ---
    mes_seleccionado = user.mes_actual
    dia_seleccionado = 1
    nivel_seleccionado = user.nivel
    
    # Intentar cargar progreso guardado de hoy
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    progreso_local = page.client_storage.get("workout_progress") or {}
    
    # Si el progreso es de otro día, lo limpiamos
    if progreso_local.get("fecha") != hoy_str:
        progreso_local = {"fecha": hoy_str, "completados": {}}
        page.client_storage.set("workout_progress", progreso_local)

    # --- ELEMENTOS DE UI DINÁMICOS ---
    lista_ejercicios = ft.Column(spacing=15)
    progreso_barra = ft.ProgressBar(value=user.entrenos_mes/20, width=300, color="#FFD700", bgcolor="#333333")
    lbl_progreso = ft.Text(f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos", size=12, color="white54")
    lbl_rutina_actual = ft.Text(f"RUTINA ACTUAL: MES {mes_seleccionado} - DIA {dia_seleccionado}", size=14, weight="bold", color="#FFD700")
    
    # Contenedor de Cardio
    cardio_container = ft.Container(
        content=ft.Column([
            ft.Text("SUGERENCIA DE CARDIO", size=12, weight="bold", color="#2196F3"),
            ft.Text("", size=11, color="white70", italic=True)
        ], spacing=2),
        padding=10, bgcolor="#1A237E", border_radius=8, visible=False
    )

    # --- LÓGICA DE PERSISTENCIA ---
    def guardar_progreso_serie(ex_id, serie_idx, valor):
        key = f"{mes_seleccionado}_{dia_seleccionado}_{ex_id}"
        if key not in progreso_local["completados"]:
            progreso_local["completados"][key] = []
        
        if valor:
            if serie_idx not in progreso_local["completados"][key]:
                progreso_local["completados"][key].append(serie_idx)
        else:
            if serie_idx in progreso_local["completados"][key]:
                progreso_local["completados"][key].remove(serie_idx)
        
        page.client_storage.set("workout_progress", progreso_local)

    def obtener_progreso_serie(ex_id, serie_idx):
        key = f"{mes_seleccionado}_{dia_seleccionado}_{ex_id}"
        completados = progreso_local["completados"].get(key, [])
        return serie_idx in completados

    # --- CRONÓMETRO DE DESCANSO ---
    overlay_timer = ft.Container(
        content=ft.Column([
            ft.Text("DESCANSO", size=16, weight="bold", color="black"),
            ft.Text("60", size=40, weight="bold", color="black"),
            ft.ProgressBar(value=1.0, width=150, color="black", bgcolor="white30")
        ], horizontal_alignment="center", spacing=5),
        bgcolor="#FFD700", padding=20, border_radius=20, 
        width=200, height=180, alignment=ft.alignment.center,
        shadow=ft.BoxShadow(blur_radius=20, color="black"),
        visible=False, animate_opacity=300, opacity=0
    )

    def iniciar_descanso(segundos):
        overlay_timer.visible = True
        overlay_timer.opacity = 1
        txt_timer = overlay_timer.content.controls[1]
        pb_timer = overlay_timer.content.controls[2]
        page.update()
        
        for i in range(segundos, -1, -1):
            if not overlay_timer.visible: break
            txt_timer.value = str(i)
            pb_timer.value = i / segundos
            page.update()
            time.sleep(1)
        
        if overlay_timer.visible:
            txt_timer.value = "¡LISTO!"
            page.update()
            time.sleep(1)
            overlay_timer.opacity = 0
            page.update()
            time.sleep(0.3)
            overlay_timer.visible = False
            page.update()

    # --- FUNCIONES DE ACTUALIZACIÓN ---
    def set_mes(n):
        nonlocal mes_seleccionado
        mes_seleccionado = n
        actualizar_ui_meses()
        update_workout_list()

    def update_workout_list(dia=None, init=False):
        nonlocal dia_seleccionado
        if dia: dia_seleccionado = dia
        
        lbl_rutina_actual.value = f"RUTINA ACTUAL: MES {mes_seleccionado} - DIA {dia_seleccionado}"
        actualizar_ui_dias()
        actualizar_cardio()
        
        exs = db.get_dynamic_exercises(client, user.genero, nivel_seleccionado, mes_seleccionado, dia_seleccionado, user.objetivo)
        lista_ejercicios.controls.clear()
        
        if not exs:
            lista_ejercicios.controls.append(ft.Container(content=ft.Text("No hay ejercicios para hoy.", color="white54"), padding=20))
        else:
            for ex in exs:
                last_w = db.get_last_weight(client, user.id, ex.nombre)
                sugerencia_txt = f"{last_w + 2.5}kg" if last_w > 0 else "Peso moderado"
                
                lbl_sugerencia = ft.Text(f"Sugerencia: {sugerencia_txt}", size=11, color="#FFD700", weight="bold")
                
                # Fila de Series (Checkboxes)
                row_series = ft.Row(wrap=True, spacing=5)
                for s_idx in range(ex.series):
                    is_checked = obtener_progreso_serie(ex.id, s_idx)
                    cb = ft.Checkbox(
                        label=f"S{s_idx+1}", 
                        value=is_checked,
                        fill_color="#FFD700",
                        on_change=lambda e, ex_id=ex.id, idx=s_idx, t=ex.descanso: 
                            (guardar_progreso_serie(ex_id, idx, e.control.value), 
                             threading.Thread(target=iniciar_descanso, args=(t,), daemon=True).start() if e.control.value else None)
                    )
                    row_series.controls.append(cb)

                txt_peso_hoy = ft.TextField(label="Kg", width=70, height=35, text_size=12, border_color="#FFD700")

                def guardar_peso(e, nombre_ex=ex.nombre, field=txt_peso_hoy, lbl=lbl_sugerencia):
                    try:
                        peso = float(field.value)
                        if db.log_pr(client, user.id, nombre_ex, peso):
                            show_snackbar(f"¡{nombre_ex} guardado!", False)
                            lbl.value = f"Sugerencia: {peso + 2.5}kg"
                            page.update()
                    except: show_snackbar("Valor inválido", True)

                lista_ejercicios.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(ex.nombre, weight="bold", size=15, expand=True),
                                ft.IconButton("timer", icon_color="#FFD700", on_click=lambda _: threading.Thread(target=iniciar_descanso, args=(ex.descanso,), daemon=True).start())
                            ]),
                            row_series,
                            ft.Row([
                                ft.Column([ft.Text(f"Reps: {ex.reps}", size=11, color="white54"), lbl_sugerencia], expand=True),
                                txt_peso_hoy,
                                ft.IconButton("save", icon_color="#4CAF50", on_click=guardar_peso)
                            ])
                        ], spacing=8),
                        padding=12, bgcolor="#1E1E1E", border_radius=12
                    )
                )
        if not init: page.update()

    def actualizar_cardio():
        msg = ""
        if user.objetivo == "Aumento de masa muscular":
            msg = "10-15 min baja intensidad (Caminata) - AL FINAL. Para salud cardíaca sin quemar músculo."
        elif user.objetivo == "Definición / Quema de Grasa":
            msg = "25-35 min intensidad moderada (LISS) - AL FINAL. Maximiza oxidación de grasas."
        else:
            msg = "20 min HIIT o intervalos - AL FINAL. Mejora resistencia."
        
        cardio_container.content.controls[1].value = msg
        cardio_container.visible = True

    # --- COMPONENTES DE NAVEGACIÓN ---
    row_meses = ft.Row(scroll="auto", spacing=10)
    def actualizar_ui_meses():
        row_meses.controls = [
            ft.ElevatedButton(
                f"MES {i}", 
                on_click=lambda e, n=i: set_mes(n) if n <= user.mes_actual else show_snackbar("Mes bloqueado", True),
                style=ft.ButtonStyle(
                    bgcolor="#FFD700" if i == mes_seleccionado else "#333333",
                    color="black" if i == mes_seleccionado else "white"
                )
            ) for i in range(1, 7)
        ]

    row_dias = ft.Row(scroll="auto", spacing=8, alignment="center")
    def actualizar_ui_dias():
        row_dias.controls = [
            ft.TextButton(
                f"DÍA {i}", 
                on_click=lambda e, n=i: update_workout_list(n),
                style=ft.ButtonStyle(
                    color="#FFD700" if i == dia_seleccionado else "white54"
                )
            ) for i in range(1, 6)
        ]

    # --- INICIALIZACIÓN ---
    actualizar_ui_meses()
    update_workout_list(init=True)

    return ft.Stack([
        ft.Column([
            ft.Text("ENTRENAMIENTO", size=22, weight="bold", color="#FFD700"),
            ft.Column([lbl_progreso, progreso_barra], horizontal_alignment="center"),
            ft.Divider(height=10, color="transparent"),
            row_meses,
            ft.Divider(height=10, color="white12"),
            row_dias,
            lbl_rutina_actual,
            cardio_container,
            ft.Container(content=lista_ejercicios, expand=True),
            ft.ElevatedButton("FINALIZAR ENTRENAMIENTO", icon="check_circle", on_click=lambda _: show_snackbar("¡Día completado! 💪", False),
                              style=ft.ButtonStyle(bgcolor="#4CAF50", color="white"), width=350, height=50),
            ft.Container(height=20)
        ], expand=True, horizontal_alignment="center", scroll="adaptive"),
        
        # Overlay del Cronómetro (Centrado)
        ft.Container(
            content=overlay_timer,
            alignment=ft.alignment.center,
            expand=True,
            # Este contenedor atrapa clics si overlay_timer es visible
            visible=False 
        )
    ])
