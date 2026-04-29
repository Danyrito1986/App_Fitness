import flet as ft
import db_manager as db

def login_view(page: ft.Page, on_login_success, show_snackbar):
    # Variables de estado
    is_login_mode = True

    # Componentes de UI
    email_field = ft.TextField(label="Correo Electrónico", prefix_icon=ft.icons.EMAIL, width=300)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, width=300)
    name_field = ft.TextField(label="Nombre Completo", prefix_icon=ft.icons.PERSON, width=300, visible=False)
    
    error_text = ft.Text(color="red", size=12)
    
    def toggle_mode(e):
        nonlocal is_login_mode
        is_login_mode = not is_login_mode
        name_field.visible = not is_login_mode
        action_button.text = "Iniciar Sesión" if is_login_mode else "Registrarse"
        toggle_button.text = "¿No tienes cuenta? Regístrate" if is_login_mode else "¿Ya tienes cuenta? Inicia Sesión"
        error_text.value = ""
        page.update()

    def handle_action(e):
        email = email_field.value
        password = password_field.value
        nombre = name_field.value
        
        if not email or not password:
            show_snackbar("Por favor, completa todos los campos.", is_error=True)
            return
            
        try:
            print(f"Intentando login para: {email}")
            if is_login_mode:
                res = db.login_user(email, password)
                # Verificamos si el objeto tiene el atributo user (compatibilidad supabase-py)
                user_obj = getattr(res, "user", None)
                if user_obj:
                    show_snackbar("¡Bienvenido de nuevo! 👋")
                    on_login_success()
                else:
                    show_snackbar("Credenciales incorrectas o error de servidor.", True)
            else:
                if not nombre:
                    show_snackbar("El nombre es obligatorio.", True)
                    return
                res = db.register_user(email, password, nombre)
                if getattr(res, "user", None):
                    show_snackbar("Registro exitoso. ¡Inicia sesión! 🎉")
                    toggle_mode(None)
        except Exception as ex:
            print(f"Error detallado en login: {ex}")
            show_snackbar(f"Error al iniciar: {str(ex)}", True)
        page.update()

    action_button = ft.ElevatedButton(
        text="Iniciar Sesión",
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700),
        on_click=handle_action,
        width=300
    )
    
    toggle_button = ft.TextButton(
        text="¿No tienes cuenta? Regístrate",
        on_click=toggle_mode
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.icons.FITNESS_CENTER, size=80, color=ft.colors.BLUE_700),
                ft.Text("Bienvenido a App Fitness", size=24, weight="bold"),
                ft.Text("Tu entrenador personal en la nube", size=14, color=ft.colors.GREY_400),
                ft.Divider(height=20, color="transparent"),
                name_field,
                email_field,
                password_field,
                error_text,
                ft.Divider(height=10, color="transparent"),
                action_button,
                toggle_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        expand=True,
        alignment=ft.alignment.center
    )
