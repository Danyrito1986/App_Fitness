import flet as ft
from models import User
from datetime import datetime
from supabase import Client
import json
import os
from services.calculator import calculate_macros

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de nutrición profesional con sistema de intercambio dinámico."""
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JSON_PATH = os.path.join(BASE_DIR, "assets", "data", "diet_plan.json")
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            diet_data = json.load(f)
        fuentes = diet_data["fuentes"]
        matriz = {int(k): v for k, v in diet_data["matriz"].items()}
    except Exception as e:
        print(f"ERROR CRÍTICO: No se pudo cargar diet_plan.json. Error: {e}")
        show_snackbar("Error al cargar datos nutricionales", True)
        return ft.Column([ft.Text("Error al cargar datos nutricionales", color="red")])

    macros = calculate_macros(user)
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']
    
    dia_semana = datetime.now().weekday()
    nombres_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    # Recuperar selecciones personalizadas de la sesión
    if not page.session.get("diet_selections"):
        page.session.set("diet_selections", {})
    
    main_column = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", spacing=15)

    def open_exchange_modal(tipo_comida, macro_key, macro_target_grams, fuente_key):
        """Abre un modal para intercambiar la fuente de un macro específico."""
        options = fuentes[fuente_key]
        selections = page.session.get("diet_selections")

        def on_select(e, idx):
            selections[f"{dia_semana}_{tipo_comida}_{macro_key}"] = idx
            page.session.set("diet_selections", selections)
            bs.open = False
            page.update()
            build_ui()

        list_tiles = []
        for i, opt in enumerate(options):
            # Calcular porción equivalente
            # Si es carbohidrato, usamos 'c', si es proteina 'p', si es grasa 'g'
            density = opt[macro_key]
            gr = int((macro_target_grams / density) * 100)
            
            desc = f"{gr}g de {opt['nombre']}"
            if opt["nombre"] == "Tortilla de Maíz":
                desc = f"{round(macro_target_grams/15, 1)} unidades de {opt['nombre']}"
            elif opt["nombre"] == "Pan Integral":
                desc = f"{round(macro_target_grams/15, 1)} rebanadas de {opt['nombre']}"

            list_tiles.append(
                ft.ListTile(
                    leading=ft.Icon(opt.get("icon", "restaurant"), color="#FFD700"),
                    title=ft.Text(opt["nombre"], weight="bold"),
                    subtitle=ft.Text(desc, color="white54"),
                    on_click=lambda e, idx=i: on_select(e, idx)
                )
            )

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.Text(f"INTERCAMBIAR {macro_key.upper()}", size=16, weight="bold"),
                        ft.IconButton(ft.icons.CLOSE, on_click=lambda _: setattr(bs, "open", False) or page.update())
                    ], alignment="spaceBetween"),
                    ft.Divider(color="white10"),
                    ft.Column(list_tiles, scroll=ft.ScrollMode.AUTO, height=400)
                ], tight=True),
                padding=20, bgcolor="#1E1E1E", border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ),
            open=True
        )
        page.overlay.append(bs)
        page.update()

    def get_alimentos_dinamicos(p_comida, c_comida, f_comida, tipo_comida):
        try:
            selections = page.session.get("diet_selections")
            indices_base = matriz.get(dia_semana, {}).get(tipo_comida, {"p": 0, "c": 0, "g": 0})
            
            idx_p = selections.get(f"{dia_semana}_{tipo_comida}_p", indices_base.get("p", 0))
            idx_c = selections.get(f"{dia_semana}_{tipo_comida}_c", indices_base.get("c", 0))
            idx_g = selections.get(f"{dia_semana}_{tipo_comida}_g", indices_base.get("g", 0))

            f_p = fuentes["proteina"][idx_p]
            f_c = fuentes["carbo"][idx_c]
            f_g = fuentes["grasa"][idx_g]

            def get_density(obj, key):
                d = obj.get(key, 0)
                return d if d > 0 else 1 # Evitar división por cero

            gr_p = int((p_comida / get_density(f_p, "p")) * 100)
            gr_c = int((c_comida / get_density(f_c, "c")) * 100)
            gr_g = int((f_comida / get_density(f_g, "g")) * 100)

            def format_desc(val, name, target, unit_val, unit_name):
                if name == unit_name:
                    return f"{round(target/unit_val, 1)} unidades de {name}"
                return f"{val}g de {name}"

            desc_p = f"{gr_p}g de {f_p['nombre']}"
            desc_c = format_desc(gr_c, f_c['nombre'], c_comida, 15, "Tortilla de Maíz")
            if f_c['nombre'] == "Pan Integral":
                desc_c = format_desc(gr_c, f_c['nombre'], c_comida, 15, "Pan Integral").replace("unidades", "rebanadas")
            desc_g = f"{gr_g}g de {f_g['nombre']}"

            return {
                "p": {"desc": desc_p, "icon": f_p.get("icon", "restaurant"), "target": p_comida, "fuente": "proteina"},
                "c": {"desc": desc_c, "icon": f_c.get("icon", "bakery_dining"), "target": c_comida, "fuente": "carbo"},
                "g": {"desc": desc_g, "icon": f_g.get("icon", "water_drop"), "target": f_comida, "fuente": "grasa"}
            }
        except Exception as e:
            print(f"DEBUG_DIET_ERROR: {e}")
            return {
                "p": {"desc": "Error en datos", "icon": "error", "target": 0, "fuente": "proteina"},
                "c": {"desc": "Error en datos", "icon": "error", "target": 0, "fuente": "carbo"},
                "g": {"desc": "Error en datos", "icon": "error", "target": 0, "fuente": "grasa"}
            }

    def card_comida_detallada(nombre, pct, icono_comida):
        p_c, c_c, f_c = p*pct, c*pct, f*pct
        ali = get_alimentos_dinamicos(p_c, c_c, f_c, nombre)
        
        def item_clickable(macro_type, info):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(info['icon'], size=16, color="#FFD700"),
                    ft.Text(info['desc'], size=13, expand=True),
                    ft.Icon(ft.icons.SWAP_HORIZ, size=14, color="white24")
                ]),
                padding=8,
                border_radius=8,
                on_click=lambda _: open_exchange_modal(nombre, macro_type, info['target'], info['fuente']),
                on_hover=lambda e: setattr(e.control, "bgcolor", "white10" if e.data == "true" else None) or e.control.update()
            )

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
                            item_clickable('p', ali['p']),
                            item_clickable('c', ali['c']),
                            item_clickable('g', ali['g']),
                        ], spacing=4),
                        padding=ft.padding.only(left=15, right=15, bottom=15)
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
                    ft.ListTile(leading=ft.Icon(ft.icons.AUTO_AWESOME, color="#FFD700"), title=ft.Text("SUPLEMENTACIÓN", weight="bold", size=18)),
                    ft.Container(content=ft.Column(items, spacing=15), padding=ft.padding.only(left=20, right=20, bottom=25))
                ]),
                bgcolor="#1E1E1E", border_radius=15, border=ft.border.all(1, "#FFD70033")
            )
        )

    def build_ui():
        main_column.controls.clear()
        main_column.controls.extend([
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

            card_comida_detallada("Desayuno", 0.30, ft.icons.BRUNCH_DINING),
            card_comida_detallada("Almuerzo", 0.40, ft.icons.LUNCH_DINING),
            card_comida_detallada("Cena", 0.30, ft.icons.DINNER_DINING),
            card_suplementacion(),
            ft.Container(height=20)
        ])
        try:
            main_column.update()
        except:
            pass

    build_ui()
    return main_column
