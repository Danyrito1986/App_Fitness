import flet as ft
from models import User
from datetime import datetime
from supabase import Client
import json
import os
from services.calculator import calculate_macros

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de nutrición profesional con variedad 21/7 y carga dinámica de datos."""
    
    # --- CARGA DINÁMICA DE DATOS (Lazy Loading para evitar errores en Render) ---
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JSON_PATH = os.path.join(BASE_DIR, "assets", "data", "diet_plan.json")
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            diet_data = json.load(f)
        fuentes = diet_data["fuentes"]
        # Convertir llaves de la matriz a enteros
        matriz = {int(k): v for k, v in diet_data["matriz"].items()}
    except Exception as e:
        print(f"ERROR CRÍTICO: No se pudo cargar diet_plan.json en {JSON_PATH}. Error: {e}")
        show_snackbar("Error al cargar datos nutricionales", True)
        return ft.Column([ft.Text("Error al cargar datos. Verifica la configuración.", color="red")])

    macros = calculate_macros(user)
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']
    
    dia_semana = datetime.now().weekday()
    nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def get_alimentos_dinamicos(p_comida, c_comida, f_comida, tipo_comida):
        """Calcula gramos de alimentos basados en el día y el TIEMPO de comida con manejo de errores."""
        try:
            indices = matriz.get(dia_semana, {}).get(tipo_comida)
            if not indices:
                raise ValueError("No hay índices para esta comida")

            f_p = fuentes["proteina"][indices.get("p", 0)]
            f_c = fuentes["carbo"][indices.get("c", 0)]
            f_g = fuentes["grasa"][indices.get("g", 0)]
        except Exception as e:
            print(f"WARN: Error en get_alimentos_dinamicos: {e}")
            return {
                "p": {"desc": "Proteína no disponible", "icon": "info"},
                "c": {"desc": "Carbohidrato no disponible", "icon": "info"},
                "g": {"desc": "Grasa no disponible", "icon": "info"}
            }

        # Cálculo de gramos con protección contra división por cero
        try:
            gr_p = int((p_comida / f_p["p"]) * 100) if f_p.get("p", 0) > 0 else 0
            gr_c = int((c_comida / f_c["c"]) * 100) if f_c.get("c", 0) > 0 else 0
            gr_g = int((f_comida / f_g["g"]) * 100) if f_g.get("g", 0) > 0 else 0
        except:
            gr_p, gr_c, gr_g = 0, 0, 0

        # Formateo
        desc_c = f"{gr_c}g de {f_c['nombre']}"
        if f_c["nombre"] == "Tortilla de Maíz":
            desc_c = f"{round(c_comida/15, 1) if c_comida else 0} unidades de {f_c['nombre']}"
        elif f_c["nombre"] == "Pan Integral":
            desc_c = f"{round(c_comida/15, 1) if c_comida else 0} rebanadas de {f_c['nombre']}"

        return {
            "p": {"desc": f"{gr_p}g de {f_p['nombre']}", "icon": f_p.get("icon", "restaurant")},
            "c": {"desc": desc_c, "icon": f_c.get("icon", "bakery_dining")},
            "g": {"desc": f"{gr_g}g de {f_g['nombre']} / Semillas", "icon": f_g.get("icon", "water_drop")}
        }

    def card_comida_detallada(nombre, pct, icono_comida):
        p_c, c_c, f_c = p*pct, c*pct, f*pct
        ali = get_alimentos_dinamicos(p_c, c_c, f_c, nombre)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(icono_comida, color="#FFD700"),
                        title=ft.Text(nombre.upper(), weight="bold", size=18),
                        subtitle=ft.Text(f"{int(cal*pct)} kcal sugeridas", color="#FFD700"),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon(ali['p']['icon'], size=16, color="white54"), ft.Text(ali['p']['desc'], size=13)]),
                            ft.Row([ft.Icon(ali['c']['icon'], size=16, color="white54"), ft.Text(ali['c']['desc'], size=13)]),
                            ft.Row([ft.Icon(ali['g']['icon'], size=16, color="white54"), ft.Text(ali['g']['desc'], size=13)]),
                        ], spacing=8),
                        padding=ft.padding.only(left=20, right=20, bottom=20)
                    )
                ]),
                bgcolor="#1E1E1E", border_radius=15
            )
        )

    def card_suplementacion():
        sup = []
        d_crea = max(5.0, round(user.peso_actual * 0.1, 1))
        sup.append(("Creatina", f"{d_crea}g", "science", "Pre-entreno o Ayunas"))
        
        if p > 120:
            sup.append(("Proteína Whey", "1.5 scoops", "local_drink", "Post-entreno"))
        else:
            sup.append(("Proteína Whey", "1 scoop", "local_drink", "Post-entreno"))
            
        if user.objetivo == "Aumento de masa muscular":
            sup.append(("Multivitamínico", "1 cápsula", "medication", "Con desayuno"))
        elif user.objetivo == "Definición / Quema de Grasa":
            sup.append(("Omega 3", "2g diarios", "water_drop", "Con comidas"))

        items = [
            ft.Row([
                ft.Icon(i, color="#FFD700", size=24),
                ft.Column([ft.Text(n, weight="bold", size=14), ft.Text(f"{d} - {h}", size=11, color="white54")], spacing=2)
            ]) for n, d, i, h in sup
        ]

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(leading=ft.Icon("auto_awesome", color="#FFD700"), title=ft.Text("SUPLEMENTACIÓN", weight="bold", size=18)),
                    ft.Container(content=ft.Column(items, spacing=15), padding=ft.padding.only(left=20, right=20, bottom=25))
                ]),
                bgcolor="#1E1E1E", border_radius=15, border=ft.border.all(1, "#FFD70033")
            )
        )

    return ft.Column([
        ft.Row([
            ft.Text("TU PLAN NUTRICIONAL", size=24, weight="bold", color="#FFD700"),
            ft.Container(content=ft.Text(nombres_dias[dia_semana].upper(), weight="bold", color="black"), padding=5, bgcolor="#FFD700", border_radius=5)
        ], alignment="spaceBetween"),
        
        ft.Container(
            content=ft.Row([
                ft.Column([ft.Text("Calorías", size=10, color="white54"), ft.Text(f"{cal}", weight="bold", size=18)]),
                ft.VerticalDivider(),
                ft.Column([ft.Text("Proteína", size=10, color="white54"), ft.Text(f"{p}g", weight="bold", color="#4CAF50")]),
                ft.Column([ft.Text("Carbs", size=10, color="white54"), ft.Text(f"{c}g", weight="bold", color="#2196F3")]),
                ft.Column([ft.Text("Grasa", size=10, color="white54"), ft.Text(f"{f}g", weight="bold", color="#FFD700")]),
            ], alignment="space-around"),
            padding=15, bgcolor="#121212", border_radius=15, border=ft.border.all(1, "white10")
        ),

        card_comida_detallada("Desayuno", 0.30, "brunch_dining"),
        card_comida_detallada("Almuerzo", 0.40, "lunch_dining"),
        card_comida_detallada("Cena", 0.30, "dinner_dining"),
        card_suplementacion(),
        ft.Container(height=20)
    ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", spacing=15)
