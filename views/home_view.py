import flet as ft
import db_manager as db
from models import User

def home_view(page: ft.Page, user: User, show_snackbar):
    """Vista de Dashboard principal."""
    macros = user.get_macros()
    stats = db.get_workout_stats(user.id)
    agua_hoy = db.get_daily_water(user.id)
    
    lbl_agua = ft.Text(f"{agua_hoy} vasos", size=20, weight="bold")
    
    def sumar_agua(e):
        if db.log_water(user.id, 1):
            nonlocal agua_hoy
            agua_hoy += 1
            lbl_agua.value = f"{agua_hoy} vasos"
            show_snackbar("¡Vaso registrado! 💧")
            page.update()

    header = ft.Container(
        content=ft.Column([
            ft.Text(f"¡Hola, {user.nombre}!", size=32, weight="bold", color="#FFD700"),
            ft.Text("Hoy es un gran día para entrenar", size=16, color="white70"),
        ])
    )

    card_calorias = ft.Container(
        content=ft.Column([
            ft.Text("Calorías de Hoy", size=14, color="white54"),
            ft.Text(f"{macros['cal']}", size=36, weight="bold", color="#FFD700"),
        ], horizontal_alignment="center"),
        padding=20, bgcolor="#1E1E1E", border_radius=20, expand=True
    )

    widget_agua = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon("water_drop", color="#42A5F5"),
                ft.Text("Hidratación", weight="bold"),
            ], alignment="center"),
            lbl_agua,
            ft.IconButton("add_circle", icon_color="#42A5F5", icon_size=40, on_click=sumar_agua),
        ], horizontal_alignment="center"),
        padding=15, bgcolor="#1E1E1E", border_radius=20, width=170
    )

    return ft.Column([
        header,
        ft.Row([card_calorias], spacing=15),
        ft.Container(height=10),
        ft.Row([widget_agua], spacing=15, alignment="center"),
        ft.Container(height=20),
        ft.Text("¿Listo para el siguiente nivel?", size=14, color="white38")
    ], scroll="auto", horizontal_alignment="center")
