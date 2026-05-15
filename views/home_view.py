import flet as ft
import db_manager as db
from models import User
from services.calculator import calculate_macros
from supabase import Client

def home_view(page: ft.Page, client: Client, user: User, show_snackbar, logout_handler):
    """Vista de Dashboard principal REDISEÑADA (Estilo Moderno/Pro)."""
    
    # --- DATOS DINÁMICOS ---
    macros = calculate_macros(user)
    stats = db.get_workout_stats(client, user.id)
    racha = db.get_streak(client, user.id)
    agua_hoy = db.get_daily_water(client, user.id)
    
    user.entrenos_mes = stats % 20
    user.mes_actual = (stats // 20) + 1

    # --- LÓGICA DE HIDRATACIÓN ---
    meta_base = max(10, user.peso_actual) * 0.035
    meta_litros = round(meta_base * (1.2 if user.nivel == "Pro" else 1.0), 2)
    meta_litros = max(0.1, meta_litros) # Evitar división por cero
    consumo_actual_l = round(agua_hoy * 0.25, 2)
    restante_l = max(0, round(meta_litros - consumo_actual_l, 2))

    # --- COMPONENTES DINÁMICOS ---
    def sumar_agua(e):
        if db.log_water(client, user.id, 1):
            nonlocal agua_hoy
            agua_hoy += 1
            show_snackbar("¡Vaso registrado! 💧", False)
            page.go("/home") # Forzar refresco visual limpio
            page.update()

    # Rutina del día
    dia_logico = (user.entrenos_mes % 5) + 1
    musculos_map = {
        1: ("Pecho y Tríceps", "⚡"),
        2: ("Espalda y Bíceps", "⚓"),
        3: ("Cuádriceps", "🦵"),
        4: ("Isquios y Glúteo", "🍑"),
        5: ("Abdomen y Core", "🛡️")
    }
    rutina_txt, emoji = musculos_map.get(dia_logico, ("Descanso", "😴"))

    # --- UI COMPONENTS (MODERN STYLE) ---
    
    header = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(f"¡Hola, {user.nombre.split()[0]}!", size=28, weight="bold", color="white"),
                ft.Text(f"Hoy toca: {rutina_txt} {emoji}", size=16, color="white70"),
            ], expand=True),
            ft.Container(
                content=ft.Icon(ft.icons.PERSON, color="#FFD700", size=30),
                bgcolor="white10", padding=10, border_radius=15
            )
        ]),
        padding=ft.padding.only(bottom=20)
    )

    # Tarjeta de Racha (Gamificación)
    card_racha = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color="#FF4500", size=30),
            ft.Column([
                ft.Text(f"{racha} DÍAS", size=20, weight="bold", color="white"),
                ft.Text("Racha Actual", size=12, color="white54"),
            ], spacing=0)
        ], alignment="center"),
        padding=15, bgcolor="white10", border_radius=20, expand=True,
        border=ft.border.all(1, "white10")
    )

    # Tarjeta de Mes/Progreso
    card_mes = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.CALENDAR_MONTH, color="#FFD700", size=30),
            ft.Column([
                ft.Text(f"MES {user.mes_actual}", size=20, weight="bold", color="white"),
                ft.Text(f"Día {dia_logico}/5", size=12, color="white54"),
            ], spacing=0)
        ], alignment="center"),
        padding=15, bgcolor="white10", border_radius=20, expand=True,
        border=ft.border.all(1, "white10")
    )

    # Widget de Calorías (Grande)
    card_calorias = ft.Container(
        content=ft.Column([
            ft.Text("OBJETIVO DIARIO", size=12, weight="bold", color="white54", letter_spacing=1.2),
            ft.Row([
                ft.Text(f"{macros['cal']}", size=48, weight="bold", color="#FFD700"),
                ft.Text("KCAL", size=16, weight="bold", color="white54"),
            ], alignment="center", vertical_alignment="baseline", spacing=5),
            ft.Row([
                ft.Text(f"P: {macros['p']}g", color="#42A5F5", size=12, weight="bold"),
                ft.Text(f"C: {macros['c']}g", color="#66BB6A", size=12, weight="bold"),
                ft.Text(f"G: {macros['g']}g", color="#FFA726", size=12, weight="bold"),
            ], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=10),
        padding=25, 
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#1E1E1E", "#2D2D2D"]
        ),
        border_radius=30, 
        border=ft.border.all(1, "white10"),
        margin=ft.margin.only(bottom=20)
    )

    # Widget de Agua (Circular/Moderno)
    widget_agua = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.icons.WATER_DROP, color="#42A5F5", size=20),
                ft.Text("HIDRATACIÓN", size=12, weight="bold", color="white54", letter_spacing=1.2),
            ], alignment="center"),
            ft.Stack([
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(consumo_actual_l, color="#42A5F5", radius=10, show_title=False),
                        ft.PieChartSection(max(0.1, restante_l), color="white10", radius=10, show_title=False),
                    ],
                    sections_space=0,
                    center_space_radius=40,
                    height=100,
                ),
                ft.Container(
                    content=ft.Text(f"{int((consumo_actual_l/meta_litros)*100)}%", size=16, weight="bold", color="white"),
                    alignment=ft.alignment.center,
                    height=100
                )
            ]),
            ft.Text(f"{consumo_actual_l}L / {meta_litros}L", size=14, weight="bold", color="white"),
            ft.IconButton(
                ft.icons.ADD_CIRCLE, 
                icon_color="#42A5F5", 
                icon_size=35, 
                on_click=sumar_agua,
                tooltip="Añadir 250ml"
            ),
        ], horizontal_alignment="center", spacing=10),
        padding=20, bgcolor="white10", border_radius=30, expand=True,
        border=ft.border.all(1, "white10")
    )

    return ft.Container(
        content=ft.Column([
            header,
            ft.Row([card_racha, card_mes], spacing=15),
            ft.Container(height=10),
            card_calorias,
            ft.Row([widget_agua], spacing=15),
            ft.Container(height=20),
            ft.TextButton(
                "CERRAR SESIÓN", 
                icon=ft.icons.LOGOUT, 
                on_click=lambda _: logout_handler(),
                style=ft.ButtonStyle(color="red400")
            ),
            ft.Container(height=40),
        ], scroll="auto", horizontal_alignment="center"),
        padding=ft.padding.only(left=5, right=5)
    )
