import flet as ft
import db_manager as db
from models import User
from supabase import Client

def profile_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de Perfil REDISEÑADA (Estilo Command Center)."""
    
    # --- UI COMPONENTS ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.icons.PERSON, size=50, color="black"),
                bgcolor="#FFD700", width=100, height=100, border_radius=50,
                alignment=ft.alignment.center
            ),
            ft.Text(user.nombre.upper(), size=22, weight="bold", color="white"),
            ft.Text(user.email if hasattr(user, 'email') else "Usuario Premium", size=14, color="white54"),
        ], horizontal_alignment="center", spacing=10),
        padding=ft.padding.only(bottom=30)
    )

    def create_stat_card(label, value, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=24),
                ft.Text(value, size=18, weight="bold", color="white"),
                ft.Text(label, size=10, weight="bold", color="white38"),
            ], horizontal_alignment="center", spacing=2),
            padding=15, bgcolor="white05", border_radius=20, expand=True,
            border=ft.border.all(1, "white10")
        )

    stats_row = ft.Row([
        create_stat_card("PESO", f"{user.peso_actual}kg", ft.icons.MONITOR_WEIGHT, "#FFD700"),
        create_stat_card("ALTURA", f"{int(user.altura)}cm", ft.icons.STRAIGHTEN, "#42A5F5"),
        create_stat_card("EDAD", f"{user.edad}", ft.icons.CAKE, "#66BB6A"),
    ], spacing=10)

    # Formulario de edición con estilo moderno
    fields_style = {
        "border_color": "white10",
        "focused_border_color": "#FFD700",
        "label_style": ft.TextStyle(color="white54"),
        "text_style": ft.TextStyle(color="white"),
        "height": 55
    }

    txt_nombre = ft.TextField(label="Nombre Completo", value=user.nombre, **fields_style)
    txt_peso = ft.TextField(label="Peso Actual (kg)", value=str(user.peso_actual), **fields_style)
    txt_objetivo = ft.Dropdown(
        label="Objetivo",
        value=user.objetivo,
        options=[
            ft.dropdown.Option("Ganar masa muscular"),
            ft.dropdown.Option("Definición / Quema de Grasa"),
            ft.dropdown.Option("Mantenimiento")
        ],
        **fields_style
    )

    def guardar_cambios(e):
        try:
            data = {
                "nombre": txt_nombre.value,
                "peso": float(txt_peso.value),
                "objetivo": txt_objetivo.value
            }
            if db.update_user_profile(client, user.id, data):
                user.nombre = data["nombre"]
                user.peso_actual = data["peso"]
                user.objetivo = data["objetivo"]
                show_snackbar("¡Perfil actualizado con éxito!", False)
                page.update()
            else:
                show_snackbar("Error al guardar cambios.", True)
        except:
            show_snackbar("Datos inválidos.", True)

    btn_guardar = ft.ElevatedButton(
        "GUARDAR CAMBIOS",
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(
            color="black",
            bgcolor="#FFD700",
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        width=300, height=50,
        on_click=guardar_cambios
    )

    return ft.Container(
        content=ft.Column([
            header,
            stats_row,
            ft.Container(height=20),
            ft.Text("CONFIGURACIÓN DE CUENTA", size=12, weight="bold", color="white54", letter_spacing=1.2),
            ft.Column([
                txt_nombre,
                txt_peso,
                txt_objetivo,
            ], spacing=15),
            ft.Container(height=20),
            btn_guardar,
            ft.Container(height=40),
        ], scroll="auto", horizontal_alignment="center"),
        expand=True
    )
