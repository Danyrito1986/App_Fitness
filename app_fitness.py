import flet as ft
import db_manager as db
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

    # CLIENTE DE SUPABASE POR SESIÓN (Evita fuga de perfiles)
    client = db.get_supabase_client()

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

    # --- CONTENEDOR DE VISTA DINAMICA ---
    container_principal = ft.Container(expand=True, padding=15, bgcolor="#121212")
    user_actual = None

    def logout_handler():
        nonlocal user_actual
        db.logout_user(client)
        user_actual = None
        nav_bar.visible = False
        container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
        page.update()

    def update_view(index):
        if not user_actual:
            return
            
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
        else:
            return

        container_principal.content = content
        page.update()

    def on_nav_change(e):
        update_view(int(e.control.selected_index))

    # Barra de navegación actualizada con 5 destinos
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

    # FLUJO INICIAL
    session_user = db.get_user(client)
    if session_user:
        user_actual = session_user
        nav_bar.visible = True
        update_view(0)
        page.add(container_principal)
    else:
        container_principal.content = login_view(page, client, on_login_success=show_main_app, show_snackbar=show_snackbar)
        page.add(container_principal)

if __name__ == "__main__":
    import os
    # Render usa la variable de entorno PORT, local usa 8550
    port = int(os.environ.get("PORT", 8551))
    # 'web_browser' es vital para que funcione como PWA en celulares
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=port, 
        assets_dir="assets"
    )
