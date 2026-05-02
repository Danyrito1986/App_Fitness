import flet as ft
import db_manager as db
import time
import threading
from models import User, Exercise
from supabase import Client
from datetime import datetime
from components.timer_overlay import TimerOverlay
from components.exercise_card import ExerciseCard
from components.cardio_panel import CardioPanel
from components.status_header import StatusHeader

def workout_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de entrenamiento avanzada con persistencia, series y cronómetro."""
    
    # --- COMPONENTES ---
    timer_overlay = TimerOverlay()
    cardio_panel = CardioPanel()
    status_header = StatusHeader(user)
    
    # --- ESTADO Y PERSISTENCIA ---
    mes_seleccionado = user.mes_actual
    dia_seleccionado = 1
    nivel_seleccionado = user.nivel
    
    # Intentar cargar progreso guardado de hoy con validación robusta
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    try:
        raw_progress = page.client_storage.get("workout_progress")
        progreso_local = raw_progress if isinstance(raw_progress, dict) else {}
    except:
        progreso_local = {}
    
    # Si el progreso es de otro día, de tipo incorrecto o está vacío para hoy, intentar recuperar de Supabase
    if not isinstance(progreso_local.get("completados"), dict) or progreso_local.get("fecha") != hoy_str:
        # Intentamos restaurar de la nube (backup de seguridad)
        try:
            datos_nube = db.get_workout_progress(client, user.id, hoy_str)
            if datos_nube and isinstance(datos_nube, dict):
                progreso_local = {"fecha": hoy_str, "completados": datos_nube}
            else:
                progreso_local = {"fecha": hoy_str, "completados": {}}
        except:
            progreso_local = {"fecha": hoy_str, "completados": {}}
        
        page.client_storage.set("workout_progress", progreso_local)

    # --- ELEMENTOS DE UI DINÁMICOS ---
    lista_ejercicios = ft.Column(spacing=15, horizontal_alignment="center")

    # --- LÓGICA DE PERSISTENCIA ---
    def guardar_progreso_serie(ex_id, serie_idx, valor, t_descanso):
        key = f"{mes_seleccionado}_{dia_seleccionado}_{ex_id}"
        if key not in progreso_local["completados"]:
            progreso_local["completados"][key] = []
        
        if valor:
            if serie_idx not in progreso_local["completados"][key]:
                progreso_local["completados"][key].append(serie_idx)
            # Iniciar descanso si se marca
            threading.Thread(target=timer_overlay.iniciar_descanso, args=(t_descanso, page), daemon=True).start()
        else:
            if serie_idx in progreso_local["completados"][key]:
                progreso_local["completados"][key].remove(serie_idx)
        
        # Guardar localmente
        page.client_storage.set("workout_progress", progreso_local)
        
        # GUARDADO EN TIEMPO REAL (NUBE) - En segundo plano para no congelar la UI
        threading.Thread(
            target=db.save_workout_progress, 
            args=(client, user.id, hoy_str, progreso_local["completados"]),
            daemon=True
        ).start()

    def obtener_progreso_serie(ex_id, serie_idx):
        key = f"{mes_seleccionado}_{dia_seleccionado}_{ex_id}"
        completados = progreso_local["completados"].get(key, [])
        return serie_idx in completados

    def finalizar_entreno(e):
        # 1. Registrar en historial general
        rutina_act = f"MES {mes_seleccionado} - DÍA {dia_seleccionado}"
        if db.log_workout(client, user.id, rutina_act):
            # 2. Respaldar progreso granular en Supabase
            db.save_workout_progress(client, user.id, hoy_str, progreso_local["completados"])
            show_snackbar("¡Día completado y respaldado! 💪", False)
        else:
            show_snackbar("Error al guardar en la nube", True)
        page.update()

    def on_timer_click(t):
        threading.Thread(target=timer_overlay.iniciar_descanso, args=(t, page), daemon=True).start()

    # --- FUNCIONES DE ACTUALIZACIÓN ---
    def set_mes(n):
        nonlocal mes_seleccionado
        mes_seleccionado = n
        actualizar_ui_meses()
        update_workout_list()

    def update_workout_list(dia=None, init=False):
        nonlocal dia_seleccionado
        if dia: dia_seleccionado = dia
        
        status_header.update_rutina(mes_seleccionado, dia_seleccionado)
        actualizar_ui_dias()
        cardio_panel.actualizar_cardio(user.objetivo)
        
        exs = db.get_dynamic_exercises(client, user.genero, nivel_seleccionado, mes_seleccionado, dia_seleccionado, user.objetivo)
        lista_ejercicios.controls.clear()
        
        if not exs:
            lista_ejercicios.controls.append(ft.Container(content=ft.Text("No hay ejercicios para hoy.", color="white54"), padding=20))
        else:
            for ex in exs:
                last_w = db.get_last_weight(client, user.id, ex.nombre)
                sugerencia_txt = f"{last_w + 2.5}kg" if last_w > 0 else "Peso moderado"
                
                def on_save_peso(e, nombre_ex, field, lbl):
                    try:
                        peso = float(field.value)
                        if db.log_pr(client, user.id, nombre_ex, peso):
                            show_snackbar(f"¡{nombre_ex} guardado!", False)
                            lbl.value = f"Sugerencia: {peso + 2.5}kg"
                            page.update()
                    except: show_snackbar("Valor inválido", True)

                card = ExerciseCard(
                    ex, 
                    obtener_progreso_serie, 
                    guardar_progreso_serie, 
                    on_save_peso, 
                    on_timer_click, 
                    sugerencia_txt
                )
                lista_ejercicios.controls.append(card)

        if not init: page.update()

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
            ft.Container(
                content=ft.Column([
                    ft.Text("ENTRENAMIENTO", size=22, weight="bold", color="#FFD700"),
                    status_header,
                    ft.Divider(height=10, color="transparent"),
                    row_meses,
                    ft.Divider(height=10, color="white12"),
                    row_dias,
                    cardio_panel,
                    lista_ejercicios,
                    ft.Container(height=20),
                    ft.ElevatedButton("FINALIZAR ENTRENAMIENTO", icon="check_circle", on_click=finalizar_entreno,
                                      style=ft.ButtonStyle(bgcolor="#4CAF50", color="white"), width=350, height=50),
                    ft.Container(height=40)
                ], horizontal_alignment="center"),
                expand=True,
                scroll="adaptive"
            )
        ], expand=True),
        timer_overlay
    ], expand=True)
