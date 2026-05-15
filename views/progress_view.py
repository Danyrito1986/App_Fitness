import flet as ft
import db_manager as db
from models import User
from supabase import Client

def progress_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de Progreso REDISEÑADA con Gráficos Modernos e Interactivos."""
    
    # --- RECUPERACIÓN DE DATOS ---
    prs = db.get_prs(client, user.id)
    historial_peso = db.get_weight_history(client, user.id)
    stats_totales = db.get_workout_stats(client, user.id)

    # --- LÓGICA DE GRÁFICOS (PRs) ---
    def get_chart_data(ejercicio):
        datos_ej = [p for p in prs if p.ejercicio_nombre == ejercicio]
        if not datos_ej: return []
        # Tomar los últimos 5 registros para no saturar
        datos_ej = sorted(datos_ej, key=lambda x: x.fecha)[-5:]
        return [ft.LineChartDataPoint(i, p.peso) for i, p in enumerate(datos_ej)]

    ejercicios_con_pr = list(set([p.ejercicio_nombre for p in prs]))
    ejercicio_actual = ejercicios_con_pr[0] if ejercicios_con_pr else "Sin datos"

    chart_container = ft.Container(expand=True)

    def update_pr_chart(e):
        nonlocal ejercicio_actual
        ejercicio_actual = e.control.value
        render_chart()

    def render_chart():
        points = get_chart_data(ejercicio_actual)
        if not points:
            chart_container.content = ft.Text("No hay suficientes datos para graficar.", color="white54")
        else:
            chart_container.content = ft.LineChart(
                data_series=[
                    ft.LineChartData(
                        data_points=points,
                        stroke_width=4,
                        color="#FFD700",
                        curved=True,
                        below_line_bgcolor="white10",
                        below_line_gradient=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=["#FFD70033", "transparent"]
                        )
                    )
                ],
                border=ft.border.all(1, "white10"),
                left_axis=ft.ChartAxis(labels_size=40),
                bottom_axis=ft.ChartAxis(labels_size=30),
                tooltip_bgcolor="black",
                expand=True
            )
        chart_container.update()

    # --- UI COMPONENTS ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Text("TU EVOLUCIÓN", size=24, weight="bold", color="white", letter_spacing=1.5),
            ft.Text("Visualiza tus récords y metas alcanzadas", size=14, color="white54"),
        ]),
        padding=ft.padding.only(bottom=20)
    )

    # Resumen Rápido (Stats)
    row_stats = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text(f"{stats_totales}", size=24, weight="bold", color="#FFD700"),
                ft.Text("ENTRENOS", size=10, weight="bold", color="white38"),
            ], horizontal_alignment="center", spacing=0),
            padding=15, bgcolor="white05", border_radius=15, expand=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Text(f"{len(prs)}", size=24, weight="bold", color="#42A5F5"),
                ft.Text("RÉCORDS PR", size=10, weight="bold", color="white38"),
            ], horizontal_alignment="center", spacing=0),
            padding=15, bgcolor="white05", border_radius=15, expand=True
        ),
    ], spacing=15)

    # Selector de Ejercicio para Gráfico
    selector_ejercicio = ft.Dropdown(
        label="Seleccionar Ejercicio",
        options=[ft.dropdown.Option(ej) for ej in ejercicios_con_pr],
        value=ejercicio_actual,
        on_change=update_pr_chart,
        border_color="white10",
        label_style=ft.TextStyle(color="white54"),
        color="white"
    )

    # Sección de Gráfico de Fuerza
    box_fuerza = ft.Container(
        content=ft.Column([
            ft.Text("PROGRESO DE FUERZA (KG)", size=12, weight="bold", color="white54"),
            selector_ejercicio,
            ft.Container(chart_container, height=200, padding=10),
        ], spacing=15),
        padding=20, bgcolor="#1E1E1E", border_radius=25, border=ft.border.all(1, "white10")
    )

    # Listado de Récords Recientes
    list_prs = ft.Column(spacing=10)
    for pr in prs[:5]: # Últimos 5
        list_prs.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.EMOJI_EVENTS, color="#FFD700", size=20),
                    ft.Column([
                        ft.Text(pr.ejercicio_nombre, weight="bold", size=14),
                        ft.Text(pr.fecha, size=10, color="white54"),
                    ], spacing=0, expand=True),
                    ft.Text(f"{pr.peso} KG", weight="bold", size=16, color="#FFD700")
                ]),
                padding=12, bgcolor="white05", border_radius=15
            )
        )

    # Inicializar gráfico
    render_chart()

    return ft.Container(
        content=ft.Column([
            header,
            row_stats,
            ft.Container(height=10),
            box_fuerza,
            ft.Container(height=20),
            ft.Text("RÉCORDS RECIENTES", size=12, weight="bold", color="white54"),
            list_prs,
            ft.Container(height=40),
        ], scroll="auto", horizontal_alignment="center"),
        expand=True
    )
