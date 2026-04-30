import flet as ft
from models import User
from datetime import datetime
from supabase import Client

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de nutrición dinámica con rotación diaria de alimentos."""
    
    macros = user.get_macros()
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']
    
    # Obtener día de la semana (0=Lunes, 6=Domingo)
    dia_semana = datetime.now().weekday()
    nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def get_alimentos_dinamicos(p_comida, c_comida, f_comida):
        """Calcula gramos de alimentos basados en el día de la semana."""
        
        # Diccionario de equivalencias (Macros por cada 100g de alimento)
        fuentes = {
            "proteina": [
                {"nombre": "Pechuga de Pollo", "p": 31, "icono": "restaurant"},
                {"nombre": "Res Magra (Bistec)", "p": 26, "icono": "kebab_dining"},
                {"nombre": "Pescado Blanco (Tilapia)", "p": 24, "icono": "set_meal"},
                {"nombre": "Pechuga de Pavo", "p": 29, "icono": "restaurant"},
                {"nombre": "Salmón Fresco", "p": 20, "icono": "set_meal"},
                {"nombre": "Atún en Agua", "p": 25, "icono": "set_meal"},
                {"nombre": "Claras de Huevo", "p": 11, "icono": "egg"}
            ],
            "carbo": [
                {"nombre": "Arroz Blanco Cocido", "c": 28, "icono": "grain"},
                {"nombre": "Papa Cocida/Horneada", "c": 20, "icono": "fiber_manual_record"},
                {"nombre": "Quinoa Cocida", "c": 21, "icono": "bakery_dining"},
                {"nombre": "Pasta Integral Cocida", "c": 25, "icono": "dinner_dining"},
                {"nombre": "Avena en Hojuelas", "c": 21, "icono": "breakfast_dining"},
                {"nombre": "Camote Horneado", "c": 24, "icono": "fiber_manual_record"},
                {"nombre": "Tortilla de Maíz", "c": 15, "icono": "circle"} # 15g por unidad aprox
            ],
            "grasa": [
                {"nombre": "Aguacate Hass", "g": 15, "icono": "eco"},
                {"nombre": "Almendras Naturales", "g": 50, "icono": "nuts"},
                {"nombre": "Aceite de Oliva Extra V.", "g": 92, "icono": "water_drop"},
                {"nombre": "Crema de Cacahuate", "g": 50, "icono": "favorite"},
                {"nombre": "Nueces de Castilla", "g": 65, "icono": "nuts"},
                {"nombre": "Pistaches", "g": 45, "icono": "nuts"},
                {"nombre": "Aceitunas", "g": 11, "icono": "eco"}
            ]
        }

        # Matriz de Rotación Semanal (Indices para el diccionario de fuentes)
        # Lunes=0, Martes=1, etc.
        rotacion = [
            {"p": 0, "c": 0, "g": 0}, # Lunes: Pollo, Arroz, Aguacate
            {"p": 1, "c": 1, "g": 1}, # Martes: Res, Papa, Almendras
            {"p": 2, "c": 2, "g": 2}, # Miércoles: Pescado, Quinoa, Oliva
            {"p": 3, "c": 3, "g": 3}, # Jueves: Pavo, Pasta, Crema Cacahuate
            {"p": 4, "c": 0, "g": 0}, # Viernes: Salmón, Arroz, Aguacate
            {"p": 5, "c": 5, "g": 4}, # Sábado: Atún, Camote, Nueces
            {"p": 6, "c": 1, "g": 2}, # Domingo: Claras, Papa, Oliva
        ]

        idx = rotacion[dia_semana]
        f_p = fuentes["proteina"][idx["p"]]
        f_c = fuentes["carbo"][idx["c"]]
        f_g = fuentes["grasa"][idx["g"]]

        # Cálculo de gramos (Regla de 3: (macro_necesario / macro_en_100g) * 100)
        gr_p = int((p_comida / f_p["p"]) * 100)
        gr_c = int((c_comida / f_c["c"]) * 100)
        gr_g = int((f_comida / f_g["g"]) * 100)

        # Ajuste especial para Tortillas o Unidades
        desc_c = f"{gr_c}g de {f_c['nombre']}"
        if f_c["nombre"] == "Tortilla de Maíz":
            unidades = round(c_comida / 15, 1)
            desc_c = f"{unidades} unidades de {f_c['nombre']}"

        return {
            "proteina": {"desc": f"{gr_p}g de {f_p['nombre']}", "icon": f_p["icono"]},
            "carbo": {"desc": desc_c, "icon": f_c["icono"]},
            "grasa": {"desc": f"{gr_g}g de {f_g['nombre']} / Semillas", "icon": f_g["icono"]}
        }

    def card_comida_detallada(nombre, pct, icono_comida):
        p_c, c_c, f_c = p*pct, c*pct, f*pct
        ali = get_alimentos_dinamicos(p_c, c_c, f_c)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(icono_comida, color="#FFD700"),
                        title=ft.Text(nombre, weight="bold", size=18),
                        subtitle=ft.Text(f"{int(cal*pct)} kcal sugeridas", color="#FFD700"),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon(ali['proteina']['icon'], size=16, color="white54"), ft.Text(ali['proteina']['desc'], size=13)]),
                            ft.Row([ft.Icon(ali['carbo']['icon'], size=16, color="white54"), ft.Text(ali['carbo']['desc'], size=13)]),
                            ft.Row([ft.Icon(ali['grasa']['icon'], size=16, color="white54"), ft.Text(ali['grasa']['desc'], size=13)]),
                        ], spacing=8),
                        padding=ft.padding.only(left=20, right=20, bottom=20)
                    )
                ]),
                bgcolor="#1E1E1E",
                border_radius=15
            )
        )

    def card_suplementacion():
        suplementos = []
        dosis_creatina = round(user.peso_actual * 0.1, 1)
        if dosis_creatina < 5: dosis_creatina = 5.0
        suplementos.append(("Creatina Monohidratada", f"{dosis_creatina}g diarios (Mantenimiento)", "science"))
        
        if p > 120:
            suplementos.append(("Proteína Whey/Isolate", "1-2 scoops (25-50g) post-entreno o snack", "local_drink"))
        else:
            suplementos.append(("Proteína Whey/Isolate", "1 scoop (25g) post-entrenamiento", "local_drink"))
            
        if user.objetivo == "Aumento de masa muscular":
            suplementos.append(("Multivitamínico", "1 cápsula con el desayuno", "medication"))
        elif user.objetivo == "Definición / Quema de Grasa":
            suplementos.append(("Cafeína / Té Verde", "200mg como pre-entreno natural", "bolt"))
            suplementos.append(("Omega 3", "2-3g diarios para salud metabólica", "water_drop"))
        
        items_ui = [
            ft.Row([
                ft.Icon(icono, color="#FFD700", size=20),
                ft.Column([ft.Text(nombre, weight="bold", size=14), ft.Text(dosis, size=12, color="white54")], spacing=2)
            ]) for nombre, dosis, icono in suplementos
        ]

        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon("auto_awesome", color="#FFD700"),
                        title=ft.Text("SUPLEMENTACIÓN INTELIGENTE", weight="bold", size=18),
                        subtitle=ft.Text("Dosis personalizadas para tu objetivo", color="white54", size=12),
                    ),
                    ft.Container(content=ft.Column(items_ui, spacing=15), padding=ft.padding.only(left=20, right=20, bottom=25))
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

        ft.Text(f"MENÚ DEL DÍA: {nombres_dias[dia_semana]}", size=12, color="white38", weight="bold"),

        card_comida_detallada("Desayuno", 0.30, "brunch_dining"),
        card_comida_detallada("Almuerzo", 0.40, "lunch_dining"),
        card_comida_detallada("Cena", 0.30, "dinner_dining"),

        ft.Divider(height=20, color="white12"),
        ft.Text("RECOMENDACIÓN TÉCNICA", size=12, color="white38", weight="bold"),
        card_suplementacion(),

        ft.Container(height=20),
        ft.Text("* Las medidas son en alimentos ya cocidos.", size=10, color="white24", italic=True)
    ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", spacing=15)

