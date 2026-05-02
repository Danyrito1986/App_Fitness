import flet as ft
import db_manager as db
from models import User, WeightHistory
from views.home_view import home_view
from views.workout_view import workout_view
from views.diet_view import diet_view
from views.progress_view import progress_view
from views.profile_view import profile_view
from views.login_view import login_view
import unittest
from unittest.mock import MagicMock, patch

class TestAppFullRobustness(unittest.TestCase):
    def setUp(self):
        # Mock de la página de Flet
        self.page = MagicMock(spec=ft.Page)
        self.page.client_storage = MagicMock()
        
        # Simular fallos constantes en storage para probar el "peor caso"
        self.page.client_storage.get.side_effect = Exception("Storage Error")
        self.page.client_storage.set.side_effect = Exception("Storage Error")
        
        # Mock del cliente de Supabase (simulando desconexión o error de red)
        self.client = MagicMock()
        
        # Usuario de prueba con datos mínimos
        self.user = User(
            id=1, nombre="Usuario Test", objetivo="Resistencia",
            peso_actual=80.0, mes_actual=1, entrenos_mes=0
        )
        
        # Callback de snackbar
        self.show_snackbar = lambda m, e=False: print(f"  [SnackBar] {'ERROR: ' if e else ''}{m}")

    def test_all_views_robustness(self):
        """Prueba que todas las vistas devuelvan un control válido incluso ante fallos de BD/Storage."""
        vistas = {
            "HOME": lambda: home_view(self.page, self.client, self.user, self.show_snackbar, lambda: None),
            "WORKOUT": lambda: workout_view(self.page, self.client, self.user, self.show_snackbar),
            "DIET": lambda: diet_view(self.page, self.client, self.user, self.show_snackbar),
            "PROGRESS": lambda: progress_view(self.page, self.client, self.user, self.show_snackbar),
            "PROFILE": lambda: profile_view(self.page, self.client, self.user, self.show_snackbar),
            "LOGIN": lambda: login_view(self.page, self.client, lambda: None, self.show_snackbar)
        }

        for nombre, generador in vistas.items():
            print(f"\n--- Probando Vista: {nombre} ---")
            try:
                # Mock de funciones de DB que podrían fallar
                with patch('db_manager.get_workout_stats', return_value=0), \
                     patch('db_manager.get_daily_water', return_value=0), \
                     patch('db_manager.get_weight_history', return_value=[]), \
                     patch('db_manager.get_workout_progress', side_effect=Exception("DB Error")), \
                     patch('db_manager.get_dynamic_exercises', side_effect=Exception("DB Error")):
                    
                    view = generador()
                    
                    # Verificación de integridad: debe devolver algo que Flet pueda renderizar
                    self.assertIsNotNone(view, f"La vista {nombre} devolvió None")
                    self.assertTrue(hasattr(view, "controls") or hasattr(view, "content"), 
                                   f"La vista {nombre} no devolvió un control válido de Flet")
                    
                    print(f"  [OK] Vista {nombre} renderizada con éxito bajo condiciones de fallo.")
            except Exception as e:
                print(f"  [FALLO CRÍTICO] Vista {nombre} colapsó: {e}")
                self.fail(f"La vista {nombre} no es robusta: {e}")

    def test_diet_plan_json_missing(self):
        """Verifica que Diet View maneje la ausencia del archivo JSON de dieta."""
        print("\n--- Probando Diet View sin archivo JSON ---")
        with patch('os.path.exists', return_value=False), \
             patch('json.load', side_effect=FileNotFoundError("Missing JSON")):
            try:
                view = diet_view(self.page, self.client, self.user, self.show_snackbar)
                self.assertIsNotNone(view)
                print("  [OK] Diet View manejó correctamente la ausencia del JSON.")
            except Exception as e:
                self.fail(f"Diet View colapsó sin el JSON: {e}")

if __name__ == "__main__":
    print("====================================================")
    print("INICIANDO PRUEBA DE ROBUSTEZ INTEGRAL (APP_FITNESS)")
    print("====================================================")
    unittest.main()
