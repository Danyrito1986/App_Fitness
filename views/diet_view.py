import flet as ft
import db_manager as db
from models import User
from supabase import Client

def diet_view(page: ft.Page, client: Client, user: User, show_snackbar):
    """Vista de Dieta REDISEÑADA (Estilo Premium/Nutricional)."""
    
    dietas = db.get_dietas(client)
    
    # --- UI COMPONENTS ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Text("PLAN NUTRICIONAL", size=24, weight="bold", color="white", letter_spacing=1.5),
            ft.Text("Optimiza tus resultados con la alimentación correcta", size=14, color="white54"),
        ]),
        padding=ft.padding.only(bottom=20)
    )

    def create_diet_card(dieta):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(dieta.tiempo.upper(), size=10, weight="bold", color="black"),
                        bgcolor="#FFD700", padding=ft.padding.symmetric(horizontal=10, vertical=3),
                        border_radius=5
                    ),
                    ft.Text(f"{dieta.cal} KCAL", size=14, weight="bold", color="#FFD700"),
                ], alignment="justify"),
                
                ft.Text(dieta.comida, size=18, weight="bold", color="white"),
                
                ft.Divider(height=10, color="white10"),
                
                ft.Row([
                    ft.Column([ft.Text("PROT", size=10, color="white38"), ft.Text(f"{dieta.p}g", size=14, weight="bold", color="#42A5F5")], spacing=2),
                    ft.Column([ft.Text("CARB", size=10, color="white38"), ft.Text(f"{dieta.c}g", size=14, weight="bold", color="#66BB6A")], spacing=2),
                    ft.Column([ft.Text("GRASA", size=10, color="white38"), ft.Text(f"{dieta.g}g", size=14, weight="bold", color="#FFA726")], spacing=2),
                ], alignment="spaceAround")
            ], spacing=10),
            padding=20,
            bgcolor="#1E1E1E",
            border_radius=20,
            border=ft.border.all(1, "white10"),
            margin=ft.margin.only(bottom=15)
        )

    list_dietas = ft.Column(spacing=0)
    if not dietas:
        list_dietas.controls.append(
            ft.Container(
                content=ft.Text("Cargando tu plan nutricional...", color="white54"),
                padding=40, alignment=ft.alignment.center
            )
        )
    else:
        for d in dietas:
            list_dietas.controls.append(create_diet_card(d))

    return ft.Container(
        content=ft.Column([
            header,
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.RESTAURANT_MENU, color="#FFD700"),
                    ft.Text("TUS COMIDAS RECOMENDADAS", size=12, weight="bold", color="white54"),
                ]),
                margin=ft.margin.only(bottom=15)
            ),
            list_dietas,
            ft.Container(height=40),
        ], scroll="auto", horizontal_alignment="center"),
        expand=True
    )
