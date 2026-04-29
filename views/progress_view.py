import flet as ft
import db_manager as db
from models import User

def progress_view(page: ft.Page, user: User, show_snackbar):
    """Vista de progreso con historial."""
    history = db.get_weight_history(user.id)
    
    return ft.Column([
        ft.Text("MI EVOLUCIÓN", size=24, weight="bold", color="#FFD700"),
        ft.Container(
            content=ft.Column([
                ft.Text("Últimos Registros", weight="bold"),
                ft.Column([ft.Text(f"Peso: {h.peso}kg - {h.fecha}") for h in history[-5:]]) if history else ft.Text("Sin datos")
            ]),
            padding=20, bgcolor="#1E1E1E", border_radius=15
        )
    ], scroll="auto", horizontal_alignment="center")
