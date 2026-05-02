import flet as ft
import db_manager as db
from models import User
from services.calculator import calculate_macros
from supabase import Client

def home_view(page: ft.Page, client: Client, user: User, show_snackbar, logout_handler):
    """Vista de Dashboard principal."""
    macros = calculate_macros(user)
    stats = db.get_workout_stats(client, user.id)
    agua_hoy = db.get_daily_water(client, user.id)

    # --- LÓGICA DE HIDRATACIÓN INTELIGENTE ---
    # Base: 35ml por kg de peso
    meta_base = user.peso_actual * 0.035
    
    # Modificador por nivel
    multiplicador_nivel = {"Novato": 1.0, "Intermedio": 1.10, "Pro": 1.20}
    meta_ajustada = meta_base * multiplicador_nivel.get(user.nivel, 1.0)
    
    # Modificador por objetivo (Definición requiere más agua)
    if user.objetivo == "Definición / Quema de Grasa":
        meta_ajustada *= 1.10
        
    meta_litros = round(meta_ajustada, 2)
    consumo_actual_l = round(agua_hoy * 0.25, 2) # Cada vaso son 250ml
    restante_l = max(0, round(meta_litros - consumo_actual_l, 2))

    lbl_restante = ft.Text(
        f"Faltan: {restante_l} L" if restante_l > 0 else "¡Meta alcanzada! 🎯", 
        size=20, weight="bold", color="#42A5F5"
    )
    lbl_detalle_agua = ft.Text(f"Meta: {meta_litros}L | Vasos: {agua_hoy}", size=12, color="white54")

    def sumar_agua(e):
        if db.log_water(client, user.id, 1):
            nonlocal agua_hoy, consumo_actual_l, restante_l
            agua_hoy += 1
            consumo_actual_l = round(agua_hoy * 0.25, 2)
            restante_l = max(0, round(meta_litros - consumo_actual_l, 2))

            lbl_restante.value = f"Faltan: {restante_l} L" if restante_l > 0 else "¡Meta alcanzada! 🎯"
            lbl_detalle_agua.value = f"Meta: {meta_litros}L | Vasos: {agua_hoy}"

            if restante_l <= 0:
                show_snackbar("¡FELICIDADES! Meta de hidratación cumplida 🎯💦", False)
            else:
                show_snackbar("¡Vaso registrado! 💧", False)
            page.update()

    # --- LÓGICA DE DÍA ACTUAL ---
    dia_actual = (user.entrenos_mes % 5) + 1
    musculos_map = {
        1: "Pecho, Hombro Frontal y Tríceps 💪",
        2: "Espalda, Bíceps y Posterior 🦅",
        3: "Cuádriceps, Glúteos y Pantorrilla 🍗",
        4: "Hombro Lateral, Trapecio y Abdomen 🛡️",
        5: "Isquiosurales, Glúteos y Brazos 🔥"
    }
    mensaje_musculos = f"Músculos de hoy: {musculos_map.get(dia_actual, '¡A darle con todo!')}"

    header = ft.Container(
        content=ft.Column([
            ft.Text(f"¡Hola, {user.nombre}!", size=32, weight="bold", color="#FFD700"),
            ft.Text(mensaje_musculos, size=16, color="white70"),
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
            lbl_restante,
            lbl_detalle_agua,
            ft.Button(icon="add_circle", icon_color="#42A5F5", on_click=sumar_agua),
        ], horizontal_alignment="center", spacing=5),
        padding=15, bgcolor="#1E1E1E", border_radius=20, width=220
    )

    return ft.Column([
        header,
        ft.Row([card_calorias], spacing=15),
        ft.Container(height=10),
        ft.Row([widget_agua], spacing=15, alignment="center"),
        ft.Container(height=10),
        ft.TextButton(
            "CERRAR SESIÓN", 
            icon="logout", 
            on_click=lambda _: logout_handler(),
            style=ft.ButtonStyle(color="red400")
        ),
        ft.Container(height=20),
        ft.Text("¿Listo para el siguiente nivel?", size=14, color="white38")
    ], scroll="auto", horizontal_alignment="center")
