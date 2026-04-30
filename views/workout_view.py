import flet as ft
import db_manager as db
import time
import threading
from models import User, Exercise

from supabase import Client

def workout_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de entrenamiento dinámica controlada desde Supabase."""
    
    # --- ESTADO ---
    mes_seleccionado = user.mes_actual
    dia_seleccionado = 1
    nivel_seleccionado = user.nivel
    
    lista_ejercicios = ft.Column(spacing=10)
    progreso_barra = ft.ProgressBar(value=user.entrenos_mes/20, width=300, color="#FFD700", bgcolor="#333333")
    lbl_progreso = ft.Text(f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos", size=12, color="white54")

    def registrar_entreno(e):
        if db.log_workout(client, user.id, f"Mes {user.mes_actual} - DIA-{dia_seleccionado}"):
            user.entrenos_mes += 1
            
            # Verificar si completó el mes
            if user.entrenos_mes >= 20:
                user.mes_actual += 1
                user.entrenos_mes = 0
                show_snackbar(f"¡FELICIDADES! 🎉 Has desbloqueado el Mes {user.mes_actual}", False)
                actualizar_ui_meses() # Refrescar botones de meses
            else:
                show_snackbar("¡Entrenamiento registrado! 💪", False)
            
            # Guardar en DB
            db.update_user_profile(client, user.id, {
                "nombre": user.nombre, "objetivo": user.objetivo, "peso": user.peso_actual,
                "mes_actual": user.mes_actual, "entrenos_mes": user.entrenos_mes,
                "genero": user.genero, "altura": user.altura, "cuello": user.cuello, 
                "cintura": user.cintura, "cadera": user.cadera, "edad": user.edad
            })
            
            progreso_barra.value = user.entrenos_mes / 20
            lbl_progreso.value = f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos"
            page.update()

    def change_nivel(e):
        nonlocal nivel_seleccionado
        nivel_seleccionado = list(e.control.selected)[0]
        update_workout_list()

    nivel_selector = ft.SegmentedButton(
        selected={nivel_seleccionado},
        on_change=change_nivel,
        segments=[
            ft.Segment("Novato", label=ft.Text("Novato")),
            ft.Segment("Intermedio", label=ft.Text("Int.")),
            ft.Segment("Pro", label=ft.Text("Pro")),
        ],
        show_selected_icon=False,
    )

    def update_workout_list(dia=None):
        nonlocal dia_seleccionado
        if dia: dia_seleccionado = dia
        
        # LLAMADA DINÁMICA A SUPABASE
        exs = db.get_dynamic_exercises(
            client,
            user.genero, 
            nivel_seleccionado, 
            mes_seleccionado, 
            dia_seleccionado,
            user.objetivo
        )
        
        lista_ejercicios.controls.clear()
        
        if not exs:
            lista_ejercicios.controls.append(
                ft.Container(
                    content=ft.Text("No hay ejercicios cargados en Supabase para este día.", color="white54", italic=True),
                    padding=20, alignment=ft.alignment.center
                )
            )
        else:
            for ex in exs:
                # Obtener último peso para sugerencia
                last_w = db.get_last_weight(client, user.id, ex.nombre)
                sugerencia = f"{last_w + 2.5}kg" if last_w > 0 else "Inicia con peso moderado"
                info_anterior = f"Anterior: {last_w}kg" if last_w > 0 else "Sin registros"

                txt_peso_hoy = ft.TextField(
                    label="Kg hoy",
                    width=80,
                    height=40,
                    text_size=12,
                    border_color="#FFD700",
                    keyboard_type=ft.KeyboardType.NUMBER
                )

                def guardar_peso_ex(e, nombre_ex=ex.nombre, field=txt_peso_hoy):
                    try:
                        peso = float(field.value)
                        if db.log_pr(client, user.id, nombre_ex, peso):
                            show_snackbar(f"¡Peso guardado para {nombre_ex}! 💪", False)
                            update_workout_list() # Refrescar para ver nueva sugerencia
                        else:
                            show_snackbar("Error al guardar peso.", True)
                    except:
                        show_snackbar("Ingresa un número válido.", True)

                lista_ejercicios.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Checkbox(fill_color="#FFD700"),
                                ft.Column([
                                    ft.Text(ex.nombre, weight="bold", size=16),
                                    ft.Text(f"{ex.series} series x {ex.reps} reps", size=12, color="white54")
                                ], expand=True),
                                ft.IconButton("timer_outlined", icon_color="#FFD700")
                            ]),
                            ft.Divider(height=1, color="white10"),
                            ft.Row([
                                ft.Column([
                                    ft.Text(info_anterior, size=10, color="white38"),
                                    ft.Text(f"Sugerencia: {sugerencia}", size=11, color="#FFD700", weight="bold"),
                                ], expand=True),
                                txt_peso_hoy,
                                ft.IconButton(
                                    icon="save", 
                                    icon_color="#4CAF50", 
                                    tooltip="Guardar peso de hoy",
                                    on_click=guardar_peso_ex
                                )
                            ], alignment="center")
                        ], spacing=10),
                        padding=12, bgcolor="#1E1E1E", border_radius=10
                    )
                )
        page.update()

    # --- SELECTOR DE MESES (Con Bloqueo y Refresco) ---
    row_meses = ft.Row(scroll="auto", spacing=10, wrap=True, alignment="center")

    def crear_btn_mes(n):
        bloqueado = n > user.mes_actual
        return ft.ElevatedButton(
            text=f"MES {n}" if not bloqueado else f"MES {n} 🔒",
            on_click=lambda _: set_mes(n) if not bloqueado else show_snackbar("Completa el mes anterior para desbloquear", True),
            style=ft.ButtonStyle(
                color="black" if not bloqueado else "white38",
                bgcolor="#FFD700" if not bloqueado else "#333333"
            ),
            width=110
        )

    def actualizar_ui_meses():
        row_meses.controls = [crear_btn_mes(i) for i in range(1, 7)]
        page.update()

    def set_mes(n):
        nonlocal mes_seleccionado
        mes_seleccionado = n
        update_workout_list()

    # --- UI LAYOUT ---
    actualizar_ui_meses()
    update_workout_list()

    return ft.Column([
        ft.Text("PROGRAMA DE ENTRENAMIENTO", size=22, weight="bold", color="#FFD700"),
        ft.Column([lbl_progreso, progreso_barra], horizontal_alignment="center"),

        ft.Divider(height=10, color="transparent"),
        nivel_selector,
        ft.Divider(height=10, color="transparent"),

        # Selector de Meses
        row_meses,
        
        ft.Divider(height=10, color="white12"),
        
        # Selector de Días
        ft.Row([
            ft.TextButton(f"DIA-{i}", on_click=lambda e, idx=i: update_workout_list(idx))
            for i in range(1, 6)
        ], alignment="center", wrap=True),
        
        ft.Text(f"RUTINA ACTUAL: MES {mes_seleccionado} - DIA {dia_seleccionado}", size=14, weight="bold", color="white70"),
        
        ft.Container(content=lista_ejercicios, expand=True),
        
        ft.ElevatedButton(
            "FINALIZAR ENTRENAMIENTO", 
            icon="check_circle",
            on_click=registrar_entreno,
            style=ft.ButtonStyle(bgcolor="#4CAF50", color="white"),
            width=350, height=50
        ),
        ft.Container(height=20)
    ], expand=True, horizontal_alignment="center", scroll="adaptive")
