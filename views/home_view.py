import flet as ft
import db_manager as db
from models import User
from services.calculator import calculate_macros
from supabase import Client

def home_view(page: ft.Page, client: Client, user: User, show_snackbar, logout_handler):
    """Vista de Dashboard principal con detección dinámica de rutina."""
    macros = calculate_macros(user)
    
    # Sincronizar estadísticas reales desde Supabase al entrar
    stats = db.get_workout_stats(client, user.id)
    user.entrenos_mes = stats % 20
    user.mes_actual = (stats // 20) + 1
    
    agua_hoy = db.get_daily_water(client, user.id)

    # --- LÓGICA DE HIDRATACIÓN INTELIGENTE ---
    meta_base = user.peso_actual * 0.035
    multiplicador_level = {"Novato": 1.0, "Intermedio": 1.10, "Pro": 1.20}
    meta_ajustada = meta_base * multiplicador_level.get(user.nivel, 1.0)
    
    if user.objetivo == "Definición / Quema de Grasa":
        meta_ajustada *= 1.10
        
    meta_litros = round(meta_ajustada, 2)
    consumo_actual_l = round(agua_hoy * 0.25, 2)
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

    # --- LÓGICA DE DÍA ACTUAL DINÁMICA ---
    # Día 1: Empuje Superior | Día 2: Jalón Superior | Día 3: Empuje Inferior | Día 4: Jalón Inferior | Día 5: Core
    dia_logico = (user.entrenos_mes % 5) + 1
    semana_logica = (user.entrenos_mes // 5) % 4 + 1
    
    musculos_map = {
        1: "Empuje Superior (Pecho/Hombro/Tríceps) ⚡",
        2: "Jalón Superior (Espalda/Bíceps) ⚓",
        3: "Empuje Inferior (Cuádriceps/Pantorrilla) 🦵",
        4: "Jalón Inferior (Isquiosurales/Glúteos) 🍑",
        5: "Core y Estabilidad (Abdomen/Lumbares) 🛡️"
    }
    
    rutina_txt = musculos_map.get(dia_logico, "¡Día de descanso o recuperación!")
    mensaje_musculos = f"Hoy toca: {rutina_txt}\n(Mes {user.mes_actual} - Sem {semana_logica} - Día {dia_logico})"

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
                ft.Icon(ft.icons.WATER_DROP, color="#42A5F5"),
                ft.Text("Hidratación", weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            lbl_restante,
            lbl_detalle_agua,
            ft.IconButton(ft.icons.ADD_CIRCLE, icon_color="#42A5F5", icon_size=40, on_click=sumar_agua),
        ], horizontal_alignment="center", spacing=5),
        padding=15, bgcolor="#1E1E1E", border_radius=20, width=220
    )

    return ft.Column([
        header,
        ft.Row([card_calorias], spacing=15),
        ft.Container(height=10),
        ft.Row([widget_agua], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=10),
        ft.TextButton(
            "CERRAR SESIÓN", 
            icon=ft.icons.LOGOUT, 
            on_click=lambda _: logout_handler(),
            style=ft.ButtonStyle(color="red400")
        ),
        ft.Container(height=20),
        ft.Text("¿Listo para el siguiente nivel?", size=14, color="white38")
    ], scroll="auto", horizontal_alignment="center")
