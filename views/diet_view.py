import flet as ft
from models import User

def diet_view(page: ft.Page, user: User, show_snackbar):
    """Vista de nutrición de precisión con desglose de alimentos y cantidades."""
    
    macros = user.get_macros()
    cal, p, c, f = macros['cal'], macros['p'], macros['c'], macros['f']

    def get_alimentos(p_comida, c_comida, f_comida):
        """Calcula gramos aproximados de alimentos básicos."""
        # Proteína: Pollo (31g P / 100g)
        gr_pollo = int((p_comida / 31) * 100)
        # Carbs: Arroz cocido (28g C / 100g)
        gr_arroz = int((c_comida / 28) * 100)
        # Grasa: Aguacate (15g G / 100g)
        gr_aguacate = int((f_comida / 15) * 100)
        
        return {
            "proteina": f"{gr_pollo}g de Pechuga de Pollo (o 4-5 claras de huevo)",
            "carbo": f"{gr_arroz}g de Arroz Blanco/Integral (o 1.5 papas medianas)",
            "grasa": f"{gr_aguacate}g de Aguacate (o 1 puño de almendras)"
        }

    def card_comida_detallada(nombre, pct, icono):
        p_c, c_c, f_c = p*pct, c*pct, f*pct
        ali = get_alimentos(p_c, c_c, f_c)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(icono, color="#FFD700"),
                        title=ft.Text(nombre, weight="bold", size=18),
                        subtitle=ft.Text(f"{int(cal*pct)} kcal sugeridas", color="#FFD700"),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon("restaurant", size=16, color="white54"), ft.Text(ali['proteina'], size=13)]),
                            ft.Row([ft.Icon("grain", size=16, color="white54"), ft.Text(ali['carbo'], size=13)]),
                            ft.Row([ft.Icon("eco", size=16, color="white54"), ft.Text(ali['grasa'], size=13)]),
                        ], spacing=8),
                        padding=ft.padding.only(left=20, right=20, bottom=20)
                    )
                ]),
                bgcolor="#1E1E1E",
                border_radius=15
            )
        )

    return ft.Column([
        ft.Text("TU PLAN NUTRICIONAL", size=24, weight="bold", color="#FFD700"),
        
        # Resumen de Macros
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

        ft.Text("DESGLOSE POR COMIDA (CANTIDADES EN GRAMOS)", size=12, color="white38", weight="bold"),

        card_comida_detallada("Desayuno", 0.30, "brunch_dining"),
        card_comida_detallada("Almuerzo", 0.40, "lunch_dining"),
        card_comida_detallada("Cena", 0.30, "dinner_dining"),

        ft.Container(height=20),
        ft.Text("* Las medidas son en alimentos ya cocidos.", size=10, color="white24", italic=True)
    ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", spacing=15)
