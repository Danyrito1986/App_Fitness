import flet as ft
from models import User
from views.home_view import home_view
from views.workout_view import workout_view
from views.diet_view import diet_view
from views.profile_view import profile_view
from views.progress_view import progress_view
from unittest.mock import MagicMock
import db_manager as db

def test_all_views():
    print("--- INICIANDO TEST DE INTEGRACIÓN DE VISTAS (Flet 0.21.2) ---")
    
    page = MagicMock(spec=ft.Page)
    page.client_storage = MagicMock()
    page.client_storage.get.return_value = {}
    
    client = MagicMock()
    user = User(id=1, nombre="Tester", objetivo="Resistencia", peso_actual=70.0)
    
    def show_snackbar(m, e): pass

    vistas = {
        "HOME": home_view,
        "WORKOUT": workout_view,
        "DIET": diet_view,
        "PROFILE": profile_view,
        "PROGRESS": progress_view
    }

    errors = 0
    for nombre, vista_func in vistas.items():
        try:
            print(f"Probando vista: {nombre}...", end=" ")
            if nombre == "HOME":
                vista_func(page, client, user, show_snackbar, lambda: None)
            else:
                vista_func(page, client, user, show_snackbar)
            print("OK ✅")
        except Exception as e:
            print(f"FALLO ❌ -> {e}")
            errors += 1

    if errors == 0:
        print("\n--- RESULTADO: TODAS LAS VISTAS SON COMPATIBLES CON 0.21.2 ---")
    else:
        print(f"\n--- RESULTADO: SE ENCONTRARON {errors} ERRORES ---")

if __name__ == "__main__":
    test_all_views()
