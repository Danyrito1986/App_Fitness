import flet as ft
import db_manager as db
from models import User
from supabase import Client

def progress_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de progreso avanzada con gráfica evolutiva de peso."""
    
    history = db.get_weight_history(client, user.id)
    
    # --- PREPARACIÓN DE DATOS PARA LA GRÁFICA ---
    data_points = []
    min_weight = 0
    max_weight = 100
    
    if history:
        weights = [h.peso for h in history]
        min_weight = min(weights) - 5
        max_weight = max(weights) + 5
        
        # Tomar los últimos 10 registros para no saturar la gráfica
        recent_history = history[-10:]
        for i, h in enumerate(recent_history):
            data_points.append(ft.LineChartDataPoint(i, h.peso))
    
    # --- COMPONENTE DE GRÁFICA ---
    chart_container = ft.Container(
        content=ft.Text("Registra tu peso en el Perfil para ver tu evolución 📈", color="white54", text_align="center"),
        padding=40, alignment=ft.Alignment(0, 0)
    )
    
    if len(data_points) > 1:
        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=data_points,
                    stroke_width=4,
                    color="#FFD700",
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.colors.with_opacity(0.1, "#FFD700"),
                    below_line_gradient=ft.LinearGradient(
                        begin=ft.Alignment(0, -1),
                        end=ft.Alignment(0, 1),
                        colors=[ft.colors.with_opacity(0.3, "#FFD700"), ft.colors.TRANSPARENT],
                    ),
                )
            ],
            border=ft.Border.all(1, "white10"),
            horizontal_grid_lines=ft.ChartGridLines(interval=2, color="white10", width=1),
            vertical_grid_lines=ft.ChartGridLines(interval=1, color="white10", width=1),
            min_y=min_weight,
            max_y=max_weight,
            animate=500,
            expand=True
        )
        chart_container = ft.Container(
            content=chart,
            height=250,
            padding=20,
            bgcolor="#1E1E1E",
            border_radius=15
        )
    elif len(data_points) == 1:
        chart_container = ft.Container(
            content=ft.Column([
                ft.Icon("show_chart", size=40, color="white24"),
                ft.Text(f"Peso inicial: {history[0].peso}kg. ¡Sigue registrando para ver la curva!", color="white54", text_align="center")
            ], horizontal_alignment="center"),
            padding=30, bgcolor="#1E1E1E", border_radius=15, alignment=ft.Alignment(0, 0)
        )

    # --- LISTA DE REGISTROS RECIENTES ---
    list_items = []
    if history:
        for h in reversed(history[-5:]):
            list_items.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("monitor_weight", color="#FFD700", size=20),
                        ft.Text(f"{h.peso} kg", weight="bold", size=16),
                        ft.Text(f"{h.fecha.split('T')[0]}", color="white54", size=12, expand=True, text_align="right")
                    ]),
                    padding=10, border_radius=10, bgcolor="white05"
                )
            )
    else:
        list_items.append(ft.Text("Aún no tienes registros de peso.", color="white38"))

    return ft.Column([
        ft.Text("MI EVOLUCIÓN", size=24, weight="bold", color="#FFD700"),
        ft.Text("Seguimiento de peso corporal", size=14, color="white54"),
        
        ft.Container(height=10),
        chart_container,
        
        ft.Container(height=20),
        ft.Text("HISTORIAL RECIENTE", size=16, weight="bold"),
        ft.Column(list_items, spacing=10),
        
        ft.Container(height=20),
        ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon("info_outline", size=16), ft.Text("Consejo PRO", weight="bold")]),
                ft.Text("Pésate siempre en ayunas, después de ir al baño, para obtener la medida más precisa.", size=12, color="white70")
            ], spacing=5),
            padding=15, bgcolor="#0D47A133", border_radius=10, border=ft.Border.all(1, "#0D47A1")
        )
    ], scroll="auto", horizontal_alignment="center", spacing=10)

