import flet as ft
import db_manager as db
from models import User
from supabase import Client
from services.calculator import calculate_macros

def progress_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de progreso profesional con Dashboard de Fuerza, Peso y Composición."""

    # --- CARGA DE DATOS INICIAL ---
    history = db.get_weight_history(client, user.id)
    all_prs = db.get_prs(client, user.id)
    total_workouts = db.get_workout_stats(client, user.id)
    macros = calculate_macros(user)
    
    # --- LOGICA DE TABS ---
    
    def tab_general():
        # Gráfica de Peso (Lógica existente mejorada)
        data_points = []
        min_w, max_weight = user.peso_actual - 5, user.peso_actual + 5
        
        if history:
            weights = [h.peso for h in history]
            min_w, max_weight = min(weights) - 2, max(weights) + 2
            for i, h in enumerate(history):
                data_points.append(ft.LineChartDataPoint(i, h.peso))

        chart_area = ft.Container(
            content=ft.Text("Registra tu peso en el Perfil para ver tu evolución 📈", color="white54", text_align="center"),
            padding=40, alignment=ft.alignment.center
        )

        if len(data_points) > 1:
            chart = ft.LineChart(
                data_series=[ft.LineChartData(data_points=data_points, stroke_width=4, color="#FFD700", curved=True,
                                             below_line_bgcolor=ft.colors.with_opacity(0.1, "#FFD700"))],
                border=ft.border.all(1, "white10"), min_y=min_w, max_y=max_weight, animate=500, expand=True
            )
            chart_area = ft.Container(content=chart, height=200, padding=10, bgcolor="#1E1E1E", border_radius=12)

        # Historial de pesajes
        list_items = []
        for h in reversed(history[-5:]):
            list_items.append(ft.Container(
                content=ft.Row([ft.Icon(ft.icons.MONITOR_WEIGHT, color="#FFD700", size=18),
                                ft.Text(f"{h.peso} kg", weight="bold"),
                                ft.Text(f"{h.fecha.split('T')[0]}", color="white54", size=12, expand=True, text_align="right")]),
                padding=10, bgcolor="white05", border_radius=8
            ))

        return ft.Column([
            ft.Row([
                ft.Container(content=ft.Column([ft.Text("Entrenos", size=10, color="white54"), ft.Text(str(total_workouts), size=20, weight="bold")], horizontal_alignment="center"), 
                           padding=15, bgcolor="#1E1E1E", border_radius=12, expand=True),
                ft.Container(content=ft.Column([ft.Text("Peso Actual", size=10, color="white54"), ft.Text(f"{user.peso_actual}kg", size=20, weight="bold")], horizontal_alignment="center"), 
                           padding=15, bgcolor="#1E1E1E", border_radius=12, expand=True),
            ], spacing=10),
            ft.Text("EVOLUCIÓN DE PESO", size=14, weight="bold", color="#FFD700"),
            chart_area,
            ft.Text("ÚLTIMOS REGISTROS", size=14, weight="bold"),
            ft.Column(list_items if list_items else [ft.Text("Sin registros", color="white38")], spacing=5)
        ], spacing=15, scroll=ft.ScrollMode.ADAPTIVE)

    def tab_fuerza():
        # Agrupar PRs por ejercicio
        prs_by_ex = {}
        for pr in all_prs:
            if pr.ejercicio_nombre not in prs_by_ex:
                prs_by_ex[pr.ejercicio_nombre] = []
            prs_by_ex[pr.ejercicio_nombre].append(pr)
        
        # Invertir para que el orden cronológico sea correcto en la gráfica (desc=True en get_prs trae nuevos primero)
        for ex in prs_by_ex:
            prs_by_ex[ex].reverse()

        chart_container = ft.Container(height=250, border_radius=12, bgcolor="#1E1E1E", padding=15, alignment=ft.alignment.center)
        
        def update_pr_chart(e):
            try:
                ex_name = e.control.value
                data_list = prs_by_ex.get(ex_name, [])
                if not data_list: return

                points = [ft.LineChartDataPoint(i, p.peso) for i, p in enumerate(data_list)]
                w_vals = [p.peso for p in data_list]
                
                # Protecciones para límites de gráfica
                y_min = min(w_vals) - 5 if w_vals else 0
                y_max = max(w_vals) + 5 if w_vals else 10
                if y_min == y_max: y_max += 10 # Evitar gráfica plana sin escala

                new_chart = ft.LineChart(
                    data_series=[ft.LineChartData(data_points=points, stroke_width=4, color="#4CAF50", curved=True)],
                    border=ft.border.all(1, "white10"),
                    min_y=max(0, y_min), max_y=y_max,
                    animate=500, expand=True
                )
                chart_container.content = new_chart
                if chart_container.page:
                    chart_container.update()
            except Exception as ex:
                print(f"DEBUG_PR_CHART_ERROR: {ex}")

        if not prs_by_ex:
            return ft.Column([
                ft.Container(height=40),
                ft.Icon(ft.icons.FITNESS_CENTER, size=50, color="white24"),
                ft.Text("Aún no tienes Récords Personales.\nRegistra tus pesos al entrenar.", text_align="center", color="white54")
            ], horizontal_alignment="center")

        dd_exercises = ft.Dropdown(
            label="Selecciona Ejercicio",
            options=[ft.dropdown.Option(ex) for ex in prs_by_ex.keys()],
            value=list(prs_by_ex.keys())[0],
            border_color="#4CAF50",
            on_change=update_pr_chart
        )
        
        # Inicializar con el primero
        first_ex = list(prs_by_ex.keys())[0]
        points = [ft.LineChartDataPoint(i, p.peso) for i, p in enumerate(prs_by_ex[first_ex])]
        chart_container.content = ft.LineChart(
            data_series=[ft.LineChartData(data_points=points, stroke_width=4, color="#4CAF50", curved=True)],
            border=ft.border.all(1, "white10"),
            min_y=min([p.peso for p in prs_by_ex[first_ex]]) - 5,
            max_y=max([p.peso for p in prs_by_ex[first_ex]]) + 5,
            animate=500, expand=True
        )

        return ft.Column([
            ft.Text("EVOLUCIÓN DE FUERZA (PRs)", size=16, weight="bold", color="#4CAF50"),
            dd_exercises,
            chart_container,
            ft.Text("Consejo: La sobrecarga progresiva es la clave del crecimiento.", size=11, color="white38", italic=True)
        ], spacing=15)

    def tab_composicion():
        def stat_box(label, val, unit, icon, color):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(label, size=10, color="white54"),
                    ft.Row([ft.Text(str(val), size=16, weight="bold"), ft.Text(unit, size=10)], spacing=2, alignment="center")
                ], horizontal_alignment="center", spacing=2),
                bgcolor="white05", padding=10, border_radius=10, expand=True
            )

        return ft.Column([
            ft.Text("COMPOSICIÓN CORPORAL", size=16, weight="bold", color="#2196F3"),
            ft.Container(
                content=ft.Row([
                    ft.Column([ft.Text("Grasa Corporal Est.", size=12, color="white54"), ft.Text(f"{macros['bf']}%", size=28, weight="bold", color="#FFD700")], horizontal_alignment="center"),
                    ft.VerticalDivider(),
                    ft.Column([ft.Text("Masa Magra", size=12, color="white54"), ft.Text(f"{macros['masa_magra']}kg", size=28, weight="bold", color="#2196F3")], horizontal_alignment="center"),
                ], alignment="spaceEvenly"),
                padding=20, bgcolor="#1E1E1E", border_radius=15
            ),
            ft.Row([
                stat_box("Pecho", user.pecho, "cm", ft.icons.ACCESSIBILITY_NEW, "#2196F3"),
                stat_box("Bíceps", user.bicep, "cm", ft.icons.EMOJI_EVENTS, "#2196F3"),
            ], spacing=10),
            ft.Row([
                stat_box("Cintura", user.cintura, "cm", ft.icons.STRAIGHTEN, "#FFD700"),
                stat_box("Glúteo", user.gluteo, "cm", ft.icons.FITNESS_CENTER, "#2196F3"),
            ], spacing=10),
            ft.Row([
                stat_box("Muslo", user.muslo, "cm", ft.icons.DIRECTIONS_WALK, "#2196F3"),
                stat_box("Cuello", user.cuello, "cm", ft.icons.PERSON, "#2196F3"),
            ], spacing=10),
        ], spacing=15)

    # --- ENSAMBLAJE DE TABS ---
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="GENERAL", icon=ft.icons.ANALYTICS, content=tab_general()),
            ft.Tab(text="FUERZA", icon=ft.icons.FITNESS_CENTER, content=tab_fuerza()),
            ft.Tab(text="MEDIDAS", icon=ft.icons.STRAIGHTEN, content=tab_composicion()),
        ],
        expand=1
    )

    return ft.Column([
        ft.Row([
            ft.Text("DASHBOARD DE PROGRESO", size=22, weight="bold", color="#FFD700"),
            ft.Icon(ft.icons.DASHBOARD_CUSTOMIZE, color="#FFD700", size=24)
        ], alignment="spaceBetween"),
        tabs
    ], expand=True, spacing=15)
