import flet as ft
import db_manager as db
from models import User
from services.calculator import calculate_macros
from supabase import Client

def home_view(page: ft.Page, client: Client, user: User, show_snackbar, logout_handler):
    """Vista de Dashboard ultra-simplificada para diagnostico de pantalla negra."""
    
    print("DEBUG_HOME: Iniciando construccion de home_view síncrona...")
    
    try:
        # Carga síncrona (si esto tarda, la app se congela un momento pero DEBE mostrar algo)
        stats = db.get_workout_stats(client, user.id)
        racha = db.get_streak(client, user.id)
        agua_hoy = db.get_daily_water(client, user.id)
        
        user.entrenos_mes = stats % 20
        user.mes_actual = (stats // 20) + 1
        dia_log = (user.entrenos_mes % 5) + 1
        
        try:
            macros = calculate_macros(user)
        except:
            macros = {"cal": 2000, "p": 150, "c": 200, "g": 60}

        # Componentes basicos
        nombre_user = user.nombre.split()[0] if user.nombre else "Atleta"
        
        # UI super simple (sin anidamientos complejos ni expand)
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"HOLA, {nombre_user.upper()}", size=30, weight="bold", color="white"),
                        ft.Text("DASHBOARD DE ENTRENAMIENTO", color="#FFD700", size=14),
                    ]),
                    padding=20,
                    bgcolor="#1E1E1E",
                    border_radius=10
                ),
                
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("RACHA", size=12, color="white54"),
                            ft.Text(f"{racha} DIAS", size=20, weight="bold", color="white")
                        ]),
                        padding=15, bgcolor="white10", border_radius=15, expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("PROGRESO", size=12, color="white54"),
                            ft.Text(f"MES {user.mes_actual}", size=20, weight="bold", color="white")
                        ]),
                        padding=15, bgcolor="white10", border_radius=15, expand=True
                    ),
                ], spacing=10),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("CALORIAS OBJETIVO", size=12, color="white54"),
                        ft.Text(f"{macros['cal']} KCAL", size=40, weight="bold", color="#FFD700"),
                        ft.Row([
                            ft.Text(f"P: {macros['p']}g", color="#42A5F5"),
                            ft.Text(f"C: {macros['c']}g", color="#66BB6A"),
                            ft.Text(f"G: {macros['g']}g", color="#FFA726"),
                        ], alignment="center", spacing=20)
                    ], horizontal_alignment="center"),
                    padding=20, bgcolor="white10", border_radius=20, border=ft.border.all(1, "amber300")
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("AGUA HOY", size=12, color="white54"),
                        ft.Text(f"{round(agua_hoy * 0.25, 2)} LITROS", size=25, weight="bold", color="blue400"),
                        ft.ElevatedButton("REGISTRAR VASO", icon=ft.icons.ADD, on_click=lambda _: show_snackbar("Usa el modulo de entrenamiento para registrar mas datos.", False))
                    ], horizontal_alignment="center"),
                    padding=20, bgcolor="white10", border_radius=20
                ),
                
                ft.Container(height=20),
                ft.TextButton("CERRAR SESION", icon=ft.icons.LOGOUT, on_click=lambda _: logout_handler()),
                ft.Container(height=40)
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    except Exception as e:
        print(f"DEBUG_HOME_CRITICAL_RENDER: {e}")
        return ft.Container(
            content=ft.Text(f"Error de renderizado: {e}", color="red"),
            padding=50
        )
