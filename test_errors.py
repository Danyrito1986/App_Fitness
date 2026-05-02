import flet as ft
import db_manager as db
from models import User
from views.workout_view import workout_view
from views.profile_view import profile_view
import unittest
from unittest.mock import MagicMock

class TestAppRobustness(unittest.TestCase):
    def setUp(self):
        # Mock de la página de Flet
        self.page = MagicMock(spec=ft.Page)
        self.page.client_storage = MagicMock()
        
        # Simular que el almacenamiento local lanza un error catastrófico
        self.page.client_storage.get.side_effect = Exception("Storage Failure")
        self.page.client_storage.set.side_effect = Exception("Storage Failure")
        
        # Mock del cliente de Supabase
        self.client = MagicMock()
        
        # Usuario de prueba
        self.user = User(
            id=1, nombre="Test User", objetivo="Aumento de masa muscular",
            peso_actual=70.0, mes_actual=1, entrenos_mes=5
        )

    def test_workout_view_catastrophic_failure(self):
        """Verifica que workout_view no crashee la app si falla el storage."""
        print("\n--- Probando Robustez en Entrenamiento ---")
        try:
            view = workout_view(self.page, self.client, self.user, lambda m, e: print(f"SnackBar: {m}"))
            self.assertIsInstance(view, (ft.Stack, ft.Container))
            print("ÉXITO: La vista de entrenamiento devolvió un control válido a pesar del fallo de storage.")
        except Exception as e:
            self.fail(f"FALLO: workout_view lanzó una excepción no controlada: {e}")

    def test_profile_view_catastrophic_failure(self):
        """Verifica que profile_view no crashee la app."""
        print("\n--- Probando Robustez en Perfil ---")
        try:
            view = profile_view(self.page, self.client, self.user, lambda m, e: print(f"SnackBar: {m}"))
            self.assertIsInstance(view, ft.Column)
            print("ÉXITO: La vista de perfil devolvió un control válido.")
        except Exception as e:
            self.fail(f"FALLO: profile_view lanzó una excepción no controlada: {e}")

if __name__ == "__main__":
    print("INICIANDO TEST DE ERRORES Y ROBUSTEZ...")
    unittest.main()
