import flet as ft
from models import User
from datetime import datetime
from supabase import Client

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de nutrición profesional con variedad 21/7 y horarios de suplementación."""
    
    macros = user.get_macros()
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']
    
    dia_semana = datetime.now().weekday()
    nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    def get_alimentos_dinamicos(p_comida, c_comida, f_comida, tipo_comida):
        """Calcula gramos de alimentos basados en el día y el TIEMPO de comida."""
        
        fuentes = {
            "proteina": [
                {"nombre": "Pechuga de Pollo", "p": 31, "icon": "restaurant"},        # 0
                {"nombre": "Res Magra (Bistec)", "p": 26, "icon": "kebab_dining"},   # 1
                {"nombre": "Pescado Blanco", "p": 24, "icon": "set_meal"},          # 2
                {"nombre": "Pechuga de Pavo", "p": 29, "icon": "restaurant"},        # 3
                {"nombre": "Salmón Fresco", "p": 20, "icon": "set_meal"},           # 4
                {"nombre": "Atún en Agua", "p": 25, "icon": "set_meal"},            # 5
                {"nombre": "Claras de Huevo", "p": 11, "icon": "egg"},              # 6
                {"nombre": "Lomo de Cerdo", "p": 27, "icon": "kebab_dining"}        # 7
            ],
            "carbo": [
                {"nombre": "Arroz Blanco", "c": 28, "icon": "grain"},               # 0
                {"nombre": "Papa Cocida", "c": 20, "icon": "fiber_manual_record"},  # 1
                {"nombre": "Quinoa Cocida", "c": 21, "icon": "bakery_dining"},      # 2
                {"nombre": "Pasta Integral", "c": 25, "icon": "dinner_dining"},     # 3
                {"nombre": "Avena en Hojuelas", "c": 21, "icon": "breakfast_dining"},# 4
                {"nombre": "Camote", "c": 24, "icon": "fiber_manual_record"},       # 5
                {"nombre": "Tortilla de Maíz", "c": 15, "icon": "circle"},          # 6
                {"nombre": "Pan Integral", "c": 45, "icon": "bakery_dining"}        # 7
            ],
            "grasa": [
                {"nombre": "Aguacate Hass", "g": 15, "icon": "eco"},                # 0
                {"nombre": "Almendras", "g": 50, "icon": "nuts"},                   # 1
                {"nombre": "Aceite de Oliva", "g": 92, "icon": "water_drop"},       # 2
                {"nombre": "Crema de Cacahuate", "g": 50, "icon": "favorite"},      # 3
                {"nombre": "Nueces", "g": 65, "icon": "nuts"},                      # 4
                {"nombre": "Aceite de Coco", "g": 99, "icon": "water_drop"},        # 5
                {"nombre": "Queso Panela", "g": 18, "icon": "restaurant"}           # 6
            ]
        }

        # MATRIZ 21/7 (Variedad absoluta por día y por tiempo)
        matriz = {
            0: { # Lunes
                "Desayuno": {"p": 6, "c": 4, "g": 1}, # Claras, Avena, Almendras
                "Almuerzo": {"p": 0, "c": 0, "g": 0}, # Pollo, Arroz, Aguacate
                "Cena": {"p": 2, "c": 1, "g": 2}      # Pescado, Papa, Oliva
            },
            1: { # Martes
                "Desayuno": {"p": 6, "c": 7, "g": 3}, # Claras, Pan, Crema Cacahuate
                "Almuerzo": {"p": 1, "c": 1, "g": 1}, # Res, Papa, Almendras
                "Cena": {"p": 3, "c": 3, "g": 0}      # Pavo, Pasta, Aguacate
            },
            2: { # Miércoles
                "Desayuno": {"p": 0, "c": 4, "g": 4}, # Pollo (desmenuzado), Avena, Nueces
                "Almuerzo": {"p": 2, "c": 2, "g": 2}, # Pescado, Quinoa, Oliva
                "Cena": {"p": 7, "c": 6, "g": 0}      # Cerdo, Tortillas, Aguacate
            },
            3: { # Jueves
                "Desayuno": {"p": 6, "c": 1, "g": 6}, # Claras, Papa, Panela
                "Almuerzo": {"p": 3, "c": 3, "g": 3}, # Pavo, Pasta, Crema Cacahuate
                "Cena": {"p": 4, "c": 0, "g": 2}      # Salmón, Arroz, Oliva
            },
            4: { # Viernes
                "Desayuno": {"p": 5, "c": 7, "g": 0}, # Atún, Pan, Aguacate
                "Almuerzo": {"p": 0, "c": 0, "g": 0}, # Pollo, Arroz, Aguacate
                "Cena": {"p": 1, "c": 5, "g": 1}      # Res, Camote, Almendras
            },
            5: { # Sábado
                "Desayuno": {"p": 6, "c": 4, "g": 3}, # Claras, Avena, Crema Cacahuate
                "Almuerzo": {"p": 5, "c": 5, "g": 4}, # Atún, Camote, Nueces
                "Cena": {"p": 0, "c": 6, "g": 2}      # Pollo, Tortillas, Oliva
            },
            6: { # Domingo
                "Desayuno": {"p": 6, "c": 7, "g": 2}, # Claras, Pan, Oliva
                "Almuerzo": {"p": 4, "c": 0, "g": 0}, # Salmón, Arroz, Aguacate
                "Cena": {"p": 2, "c": 1, "g": 6}      # Pescado, Papa, Panela
            }
        }

        indices = matriz[dia_semana][tipo_comida]
        f_p, f_c, f_g = fuentes["proteina"][indices["p"]], fuentes["carbo"][indices["c"]], fuentes["grasa"][indices["g"]]

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


