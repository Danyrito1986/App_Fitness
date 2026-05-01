import flet as ft
from models import User
from datetime import datetime
from supabase import Client
import json
import os
from services.calculator import calculate_macros

# Cargar datos nutricionales una sola vez al importar el módulo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "assets", "data", "diet_plan.json")

try:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        DIET_DATA = json.load(f)
    FUENTES = DIET_DATA["fuentes"]
    # Convertir llaves de la matriz a enteros
    MATRIZ = {int(k): v for k, v in DIET_DATA["matriz"].items()}
except Exception as e:
    print(f"Error cargando diet_plan.json: {e}")
    FUENTES = {"proteina": [], "carbo": [], "grasa": []}
    MATRIZ = {}

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de nutrición profesional con variedad 21/7 y horarios de suplementación."""
    
    macros = calculate_macros(user)
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']
    
    dia_semana = datetime.now().weekday()
    nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def get_alimentos_dinamicos(p_comida, c_comida, f_comida, tipo_comida):
        """Calcula gramos de alimentos basados en el día y el TIEMPO de comida."""
        
        try:
            indices = MATRIZ[dia_semana][tipo_comida]
            f_p = FUENTES["proteina"][indices["p"]]
            f_c = FUENTES["carbo"][indices["c"]]
            f_g = FUENTES["grasa"][indices["g"]]
        except KeyError:
            return {
                "p": {"desc": "Error datos", "icon": "error"},
                "c": {"desc": "Error datos", "icon": "error"},
                "g": {"desc": "Error datos", "icon": "error"}
            }

        # Cálculo de gramos
        gr_p = int((p_comida / f_p["p"]) * 100)
        gr_c = int((c_comida / f_c["c"]) * 100)
        gr_g = int((f_comida / f_g["g"]) * 100)

        # Formateo de Carbohidratos (Tortillas/Pan)
        desc_c = f"{gr_c}g de {f_c['nombre']}"
        if f_c["nombre"] == "Tortilla de Maíz":
            desc_c = f"{round(c_comida/15, 1)} unidades de {f_c['nombre']}"
        elif f_c["nombre"] == "Pan Integral":
            desc_c = f"{round(c_comida/15, 1)} rebanadas de {f_c['nombre']}"

        return {
            "p": {"desc": f"{gr_p}g de {f_p['nombre']}", "icon": f_p["icon"]},
            "c": {"desc": desc_c, "icon": f_c["icon"]},
            "g": {"desc": f"{gr_g}g de {f_g['nombre']} / Semillas", "icon": f_g["icon"]}
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
        d_crea = round(user.peso_actual * 0.1, 1)
        if d_crea < 5: d_crea = 5.0
        
        sup.append(("Creatina Monohidratada", f"{d_crea}g", "science", "En ayunas o con el pre-entreno"))
        
        if p > 120:
            sup.append(("Proteína Whey/Isolate", "1.5 scoops", "local_drink", "Inmediatamente después de entrenar"))
        else:
            sup.append(("Proteína Whey/Isolate", "1 scoop", "local_drink", "Post-entrenamiento o entre comidas"))
            
        if user.objetivo == "Aumento de masa muscular":
            sup.append(("Multivitamínico", "1 cápsula", "medication", "Con el desayuno"))
        elif user.objetivo == "Definición / Quema de Grasa":
            sup.append(("Omega 3", "2-3g diarios", "water_drop", "Repartido con almuerzo y cena"))
            sup.append(("Cafeína / Té Verde", "200mg", "bolt", "30 min antes del entrenamiento"))

        items = [
            ft.Row([
                ft.Icon(i, color="#FFD700", size=24),
                ft.Column([
                    ft.Text(n, weight="bold", size=14),
                    ft.Text(f"{d} - Horario: {h}", size=11, color="white54")
                ], spacing=2)
            ]) for n, d, i, h in sup
        ]

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon("auto_awesome", color="#FFD700"),
                        title=ft.Text("GUÍA DE SUPLEMENTACIÓN", weight="bold", size=18),
                        subtitle=ft.Text("Optimiza tus resultados con estos horarios", color="white54", size=12),
                    ),
                    ft.Container(content=ft.Column(items, spacing=15), padding=ft.padding.only(left=20, right=20, bottom=25))
                ]),
                bgcolor="#1E1E1E", border_radius=15, border=ft.border.all(1, "#FFD70033")
            )
        )

    return ft.Column([
        ft.Row([
            ft.Text("TU PLAN NUTRICIONAL", size=24, weight="bold", color="#FFD700"),
            ft.Container(
                content=ft.Text(nombres_dias[dia_semana].upper(), size=10, weight="bold", color="black"),
                padding=5, bgcolor="#FFD700", border_radius=5
            )
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

        ft.Text(f"MENÚ DINÁMICO: {nombres_dias[dia_semana]}", size=12, color="white38", weight="bold"),

        card_comida_detallada("Desayuno", 0.30, "brunch_dining"),
        card_comida_detallada("Almuerzo", 0.40, "lunch_dining"),
        card_comida_detallada("Cena", 0.30, "dinner_dining"),

        ft.Divider(height=20, color="white12"),
        card_suplementacion(),

        ft.Container(height=20),
        ft.Text("* Las medidas son en alimentos ya cocidos.", size=10, color="white24", italic=True)
    ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", spacing=15)
