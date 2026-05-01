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
    page.window_width = 420
    page.window_height = 800

    # Pantalla de Carga Inicial (Para que Render detecte la app viva de inmediato)
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
            action="Cerrar",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()

    # --- VARIABLES DE ESTADO ---
    container_principal = ft.Container(expand=True, padding=15, bgcolor="#121212")
    user_actual = None
    client = None

    def logout_handler():
        nonlocal user_actual
        if client:
            db.logout_user(client)
        user_actual = None
        nav_bar.visible = False
        container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
        page.update()

    def update_view(index):
        if not user_actual: return
        
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

        container_principal.content = content
        page.update()

    def on_nav_change(e):
        update_view(int(e.control.selected_index))

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
                nav_bar.visible = True
                nav_bar.selected_index = 0
                update_view(0)
            else:
                show_snackbar("Error al cargar perfil.", True)
        except Exception as e:
            show_snackbar(f"Error: {e}", True)
        page.update()

    def inicializar_conexion():
        """Conecta a Supabase en segundo plano sin bloquear el arranque."""
        nonlocal client, user_actual
        try:
            print("INFO: Estableciendo conexión con Supabase...")
            client = db.get_supabase_client()
            session_user = db.get_user(client)
            
            # Limpiar pantalla de carga
            page.controls.clear()
            
            if session_user:
                print(f"INFO: Sesión recuperada para {session_user.nombre}")
                user_actual = session_user
                nav_bar.visible = True
                update_view(0)
                page.add(container_principal)
            else:
                print("INFO: No hay sesión activa, mostrando Login.")
                container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
                page.add(container_principal)
            
            page.update()
        except Exception as e:
            print(f"ERROR CRÍTICO: {e}")
            page.controls.clear()
            page.add(ft.Text(f"Error de conexión: {e}", color="red"))
            page.update()

    # Disparar inicialización asíncrona
    threading.Thread(target=inicializar_conexion, daemon=True).start()

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8551))
        
        # FORZAR BINDING PARA RENDER (Garantiza que use 0.0.0.0 y el puerto correcto)
        os.environ["FLET_SERVER_IP"] = "0.0.0.0"
        os.environ["FLET_SERVER_PORT"] = str(port)
        
        print(f"--- INICIANDO SERVIDOR WEB EN 0.0.0.0:{port} ---")
        
        ft.app(
            target=main, 
            view=None, # IMPORTANTE: 'None' deshabilita apertura de ventanas y activa modo servidor
            port=port, 
            host="0.0.0.0", 
            assets_dir="assets"
        )
    except Exception as e:
        print("\n" + "!"*50)
        print("ERROR FATAL AL ARRANCAR:")
        traceback.print_exc()
        print("!"*50 + "\n")
        sys.exit(1)
