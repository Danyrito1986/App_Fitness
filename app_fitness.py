import flet as ft
import db_manager as db
import os
import traceback
import sys
import threading
from models import User
from views.home_view import home_view
from views.workout_view import workout_view
from views.diet_view import diet_view
from views.progress_view import progress_view
from views.profile_view import profile_view
from views.login_view import login_view

def main(page: ft.Page):
    # --- CONFIGURACION DE LA PAGINA ---
    page.title = "App Fitness V7 - PRO"
    page.theme_mode = "dark"
    page.bgcolor = "#121212"
    page.padding = 0
    
    # Revertir a propiedades clásicas de Flet 0.21.x
    page.window_width = 420
    page.window_height = 800

    # Pantalla de Carga Inicial
    loading_screen = ft.Container(
        content=ft.Column([
            ft.ProgressRing(color="#FFD700"),
            ft.Text("Iniciando App Fitness...", color="white54")
        ], horizontal_alignment="center", alignment="center"),
        expand=True,
        bgcolor="#121212"
    )
    page.add(loading_screen)
    page.update()

    # --- SISTEMA DE NOTIFICACIONES ---
    def show_snackbar(message: str, is_error: bool = False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor="red700" if is_error else "green700",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()

    # --- VARIABLES DE ESTADO ---
    container_principal = ft.Container(expand=True, padding=15, bgcolor="#121212")
    user_actual = None
    client = None
    vistas_cache = {}

    def logout_handler():
        nonlocal user_actual
        if client:
            db.logout_user(client)
        user_actual = None
        vistas_cache.clear()
        nav_bar.visible = False
        container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
        page.update()

    def update_view(index):
        if not user_actual: return
        
        if index in vistas_cache and index != 2:
            content = vistas_cache[index]
        else:
            if index == 0:
                content = home_view(page, client, user_actual, show_snackbar, logout_handler)
            elif index == 1:
                content = profile_view(page, client, user_actual, show_snackbar)
            elif index == 2:
                content = workout_view(page, client, user_actual, show_snackbar)
            elif index == 3:
                content = diet_view(page, client, user_actual, show_snackbar)
            elif index == 4:
                content = progress_view(page, client, user_actual, show_snackbar)
            else: return
            
            if index != 2: vistas_cache[index] = content

        container_principal.content = content
        page.update()

    def on_nav_change(e):
        update_view(int(e.control.selected_index))

    # Revertir a ft.NavigationDestination
    nav_bar = ft.NavigationBar(
        bgcolor="#1E1E1E",
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationDestination(icon="home", label="Inicio"),
            ft.NavigationDestination(icon="person", label="Perfil"),
            ft.NavigationDestination(icon="fitness_center", label="Entreno"),
            ft.NavigationDestination(icon="restaurant", label="Dieta"),
            ft.NavigationDestination(icon="show_chart", label="Progreso"),
        ],
        visible=False
    )
    page.navigation_bar = nav_bar

    def show_main_app():
        nonlocal user_actual
        try:
            user_actual = db.get_user(client)
            if user_actual:
                vistas_cache.clear()
                nav_bar.visible = True
                nav_bar.selected_index = 0
                update_view(0)
            else:
                show_snackbar("Error al cargar perfil.", True)
        except Exception as e:
            show_snackbar(f"Error: {e}", True)
        page.update()

    def inicializar_conexion():
        nonlocal client, user_actual
        try:
            client = db.get_supabase_client()
            session_user = db.get_user(client)
            page.controls.clear()
            if session_user:
                user_actual = session_user
                nav_bar.visible = True
                page.add(container_principal)
                update_view(0)
            else:
                page.add(container_principal)
                container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
            page.update()
        except Exception as e:
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.SIGNAL_WIFI_OFF, size=60, color="red700"),
                        ft.Text("Error de conexión", size=20, weight="bold"),
                        ft.ElevatedButton("Reintentar ahora", icon=ft.icons.REFRESH, on_click=lambda _: inicializar_conexion())
                    ], horizontal_alignment="center", alignment="center"),
                    expand=True, alignment=ft.alignment.center
                )
            )
            page.update()

    threading.Thread(target=inicializar_conexion, daemon=True).start()

if __name__ == "__main__":
    try:
        # Volver al arranque clásico para Render
        port = int(os.environ.get("PORT", 8551))
        
        ft.app(
            target=main,
            view=None,
            port=port,
            host="0.0.0.0",
            assets_dir="assets"
        )
    except Exception as e:
        print("\nERROR FATAL AL ARRANCAR:")
        traceback.print_exc()
        sys.exit(1)
