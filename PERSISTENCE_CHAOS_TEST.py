import unittest
import flet as ft
from unittest.mock import MagicMock, patch
import db_manager as db
from models import User, Exercise
from views.workout_view import workout_view
from datetime import datetime

class PersistenceChaosTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        # Simular almacenamiento local con datos previos
        self.storage_data = {
            "workout_progress": {
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "completados": {"1_1_1_99": [0, 1]} # Serie 0 y 1 completadas
            }
        }
        self.mock_page.client_storage.get.side_effect = lambda k: self.storage_data.get(k)
        self.mock_page.client_storage.set.side_effect = lambda k, v: self.storage_data.update({k: v})
        
        self.mock_client = MagicMock()
        # Usuario con progreso "desactualizado" en la tabla (Mes 1, Día 0)
        self.user = User(
            id=1, nombre="Test User", objetivo="Masa", peso_actual=70, 
            mes_actual=1, entrenos_mes=0
        )

    def test_01_shield_against_network_failure(self):
        """CAOS: Simula fallo de red al cargar progreso. No debe borrar la caché local."""
        print("\n  - Escenario: Fallo de red (DB devuelve None)...")
        
        with patch('db_manager.get_workout_progress') as mock_get_db, \
             patch('db_manager.get_dynamic_exercises') as mock_exs:
            
            # Simular error de conexión (None)
            mock_get_db.return_value = None 
            mock_exs.return_value = []
            
            # Lanzar la vista
            workout_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            
            # VERIFICACIÓN: El progreso local NO debe haberse borrado
            progreso_actual = self.storage_data.get("workout_progress")
            self.assertIsNotNone(progreso_actual)
            self.assertEqual(len(progreso_actual["completados"]), 1, "La caché local se borró tras fallo de red")
            print("  [PASSED] Caché local protegida contra fallos de red.")

    def test_02_dynamic_progress_calculation(self):
        """CAOS: Verifica que el progreso se calcule desde el historial, no desde el perfil estático."""
        print("  - Escenario: Perfil desincronizado vs Historial Real...")
        
        with patch('db_manager.get_workout_stats') as mock_stats:
            
            # Simular que el usuario tiene 22 entrenamientos en el historial (Mes 2, Día 2)
            # Pero su tabla 'usuarios' dice Mes 1, Día 0 (por desincronización previa)
            mock_stats.return_value = 22
            
            # Mock del cliente de Supabase para que devuelva datos desactualizados
            mock_client = MagicMock()
            mock_client.auth.get_user.return_value.user.email = "test@test.com"
            
            # Configuramos el mock para que el .execute() devuelva los datos de la tabla
            mock_response = MagicMock()
            mock_response.data = [{
                "id": 1, 
                "email": "test@test.com", 
                "nombre": "Test", 
                "mes_actual": 1, 
                "entrenos_mes": 0,
                "objetivo": "Aumento de masa muscular",
                "peso_actual": 70.0
            }]
            mock_client.table().select().eq().limit().execute.return_value = mock_response
            
            # Ejecutar la función REAL de db_manager
            user_fix = db.get_user(mock_client)
            
            # VERIFICACIÓN: El usuario debe tener Mes 2 y 2 entrenos (calculados de 22)
            self.assertEqual(user_fix.mes_actual, 2, f"Mes incorrecto: {user_fix.mes_actual}")
            self.assertEqual(user_fix.entrenos_mes, 2, f"Día incorrecto: {user_fix.entrenos_mes}")
            print("  [PASSED] Progreso calculado dinámicamente con éxito.")

    def test_03_empty_db_vs_null_db(self):
        """CAOS: Verifica que una DB vacía SÍ limpie la caché, pero un error NO."""
        print("  - Escenario: DB vacía (Limpieza legítima) vs Error (Protección)...")
        
        with patch('db_manager.get_workout_progress') as mock_get_db:
            # 1. Caso Error: No debe limpiar
            mock_get_db.return_value = None
            workout_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            self.assertTrue(len(self.storage_data["workout_progress"]["completados"]) > 0)
            
            # 2. Caso Vacío (Exitoso): Debe limpiar (porque es un nuevo día o se borró a propósito)
            # Cambiamos la fecha para forzar la lógica de inicialización
            self.storage_data["workout_progress"]["fecha"] = "2000-01-01" 
            mock_get_db.return_value = {} # DB dice que no hay nada hoy
            
            workout_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            self.assertEqual(len(self.storage_data["workout_progress"]["completados"]), 0)
            print("  [PASSED] El sistema distingue correctamente entre 'Sin datos' y 'Error de red'.")

if __name__ == "__main__":
    print("\n" + "🛡️"*15)
    print("INICIANDO PERSISTENCE CHAOS TEST")
    print("🛡️"*15)
    unittest.main()
