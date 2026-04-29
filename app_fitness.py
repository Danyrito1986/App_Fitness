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

    def update_view(index):
        if not user_actual:
            return
            
        vistas = [
            home_view(page, user_actual, show_snackbar),
            profile_view(page, user_actual, show_snackbar),
            workout_view(page, user_actual, show_snackbar),
            diet_view(page, user_actual, show_snackbar),
            progress_view(page, user_actual, show_snackbar),
        ]
        container_principal.content = vistas[index]
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
            user_actual = db.get_user()
            if user_actual:
                nav_bar.visible = True
                update_view(0)
            else:
                page.add(ft.Text("Error al cargar perfil.", color="red"))
        except Exception as e:
            show_snackbar(f"Error: {e}", True)
        page.update()

    # FLUJO INICIAL
    session_user = db.get_user()
    if session_user:
        user_actual = session_user
        nav_bar.visible = True
        update_view(0)
        page.add(container_principal)
    else:
        container_principal.content = login_view(page, on_login_success=show_main_app, show_snackbar=show_snackbar)
        page.add(container_principal)

if __name__ == "__main__":
    import os
    # Render usa la variable de entorno PORT, local usa 8550
    port = int(os.environ.get("PORT", 8550))
    # 'web_browser' es vital para que funcione como PWA en celulares
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        host="0.0.0.0", 
        port=port, 
        assets_dir="assets"
    )
