import flet as ft
import db_manager as db
import time
import threading
from models import User, Exercise

def workout_view(page: ft.Page, user: User, show_snackbar):
    """Vista de entrenamiento dinámica controlada desde Supabase (Igual que la app de Barbería)."""
    
    # --- ESTADO ---
    mes_seleccionado = user.mes_actual
    dia_seleccionado = 1
    nivel_seleccionado = user.nivel
    
    lista_ejercicios = ft.Column(spacing=10)
    progreso_barra = ft.ProgressBar(value=user.entrenos_mes/20, width=300, color="#FFD700", bgcolor="#333333")
    lbl_progreso = ft.Text(f"Progreso Mes {user.mes_actual}: {user.entrenos_mes}/20 entrenos", size=12, color="white54")

    def registrar_entreno(e):
        if db.log_workout(user.id, f"Mes {user.mes_actual} - DIA-{dia_seleccionado}"):
            user.entrenos_mes += 1
            
            # Verificar si completó el mes
            if user.entrenos_mes >= 20:
                user.mes_actual += 1
                user.entrenos_mes = 0
                show_snackbar(f"¡FELICIDADES! 🎉 Has desbloqueado el Mes {user.mes_actual}", False)
            else:
                show_snackbar("¡Entrenamiento registrado! 💪", False)
            
            # Guardar en DB
            db.update_user_profile(user.id, {
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
        
        # LLAMADA DINÁMICA A SUPABASE (Patrón Barbería)
        exs = db.get_dynamic_exercises(
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
                lista_ejercicios.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Checkbox(fill_color="#FFD700"),
                            ft.Column([
                                ft.Text(ex.nombre, weight="bold", size=16),
                                ft.Text(f"{ex.series} series x {ex.reps} reps", size=12, color="white54")
                            ], expand=True),
                            ft.IconButton("timer_outlined", icon_color="#FFD700")
                        ]),
                        padding=10, bgcolor="#1E1E1E", border_radius=10
                    )
                )
        page.update()

    # --- SELECTOR DE MESES (Con Bloqueo) ---
    def crear_btn_mes(n):
        bloqueado = n > user.mes_actual
        return ft.ElevatedButton(
            text=f"MES {n}" if not bloqueado else f"MES {n} 🔒",
            on_click=lambda _: set_mes(n) if not bloqueado else show_snackbar("Completa el mes anterior para desbloquear", True),
            style=ft.ButtonStyle(
                color="black" if not bloqueado else "white38",
                bgcolor="#FFD700" if not bloqueado else "#333333"
            ),
            width=100
        )

    def set_mes(n):
        nonlocal mes_seleccionado
        mes_seleccionado = n
        update_workout_list()

    # --- UI LAYOUT ---
    update_workout_list()

    return ft.Column([
        ft.Text("PROGRAMA DE ENTRENAMIENTO", size=22, weight="bold", color="#FFD700"),
        ft.Column([lbl_progreso, progreso_barra], horizontal_alignment="center"),

        ft.Divider(height=10, color="transparent"),
        nivel_selector,
        ft.Divider(height=10, color="transparent"),

        # Selector de Meses (Scroll Horizontal)
        ft.Row([crear_btn_mes(i) for i in range(1, 7)], scroll="auto", spacing=10),
        
        ft.Divider(height=10, color="white12"),
        
        # Selector de Días
        ft.Row([
            ft.TextButton(f"DIA-{i}", on_click=lambda e, idx=i: update_workout_list(idx))
            for i in range(1, 6)
        ], alignment="center"),
        
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
