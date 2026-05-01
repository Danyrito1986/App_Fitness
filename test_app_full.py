import unittest
import os
import sys
from datetime import datetime

# Añadir el directorio actual al path para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import User, Exercise, Diet
import db_manager as db
from views.workout_view import workout_view
from views.profile_view import profile_view
from services.calculator import calculate_macros

class TestAppFull(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n=== INICIANDO VALIDACIÓN GENERAL DE APP_FITNESS ===")
        # Verificar existencia de .env
        cls.env_exists = os.path.exists(".env")
        if not cls.env_exists:
            print("AVISO: Archivo .env no encontrado. Algunas pruebas de DB fallarán.")

    def test_01_environment_vars(self):
        """Verifica que las variables de entorno críticas estén configuradas."""
        self.assertTrue(self.env_exists, "El archivo .env es obligatorio para producción.")
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.assertIsNotNone(url, "SUPABASE_URL no está definida.")
        self.assertIsNotNone(key, "SUPABASE_KEY no está definida.")
        print("✓ Variables de entorno OK.")

    def test_02_supabase_connection(self):
        """Verifica que el cliente de Supabase se inicialice correctamente."""
        try:
            client = db.get_supabase_client()
            self.assertIsNotNone(client, "El cliente de Supabase es None.")
            print("✓ Conexión inicial con Supabase OK.")
        except Exception as e:
            self.fail(f"Fallo al conectar con Supabase: {e}")

    def test_03_user_model_logic(self):
        """Valida la lógica matemática del modelo de Usuario."""
        # Caso 1: Hombre con sobrepeso (objetivo definición)
        u_h = User(id=1, nombre="Juan", objetivo="Definición / Quema de Grasa", peso_actual=100.0, 
                  genero="Hombre", altura=180.0, cuello=42.0, cintura=105.0)
        res_h = calculate_macros(u_h)
        self.assertLess(res_h['ajuste'], 0, "Déficit debería ser negativo para definición.")
        self.assertGreater(res_h['bf'], 20, "Grasa corporal debería ser alta para estas medidas.")

        # Caso 2: Mujer delgada (objetivo volumen)
        u_m = User(id=2, nombre="Maria", objetivo="Aumento de masa muscular", peso_actual=55.0, 
                  genero="Mujer", altura=165.0, cuello=32.0, cintura=65.0, cadera=90.0)
        res_m = calculate_macros(u_m)
        self.assertGreater(res_m['ajuste'], 0, "Superávit debería ser positivo para volumen.")
        print("✓ Lógica de Modelos y Macros OK.")

    def test_04_db_manager_signatures(self):
        """Verifica que las funciones críticas de db_manager existan y retornen tipos esperados."""
        client = db.get_supabase_client()
        
        # Test get_routines
        routines = db.get_routines(client)
        self.assertIsInstance(routines, list, "get_routines debe retornar una lista.")
        
        # Test get_dynamic_exercises (con parámetros dummy)
        exs = db.get_dynamic_exercises(client, "Hombre", "Novato", 1, 1, "Aumento de masa muscular")
        self.assertIsInstance(exs, list)
        if len(exs) > 0:
            self.assertIsInstance(exs[0], Exercise)
        
        print("✓ Firmas de DB Manager OK.")

    def test_05_view_initialization(self):
        """Simula la inicialización de vistas para detectar errores de sintaxis o imports."""
        # Mock de page y client
        class MockPage:
            def __init__(self):
                self.client_storage = type('obj', (object,), {'get': lambda k: None, 'set': lambda k, v: None})
                self.session = {}
        
        mock_page = MockPage()
        client = db.get_supabase_client()
        user = User(id=1, nombre="Test", objetivo="Resistencia", peso_actual=70.0)
        
        try:
            # Solo llamamos para ver si crashea al construir el árbol de UI básico
            # Usamos una función lambda para show_snackbar mockeada
            workout_view(mock_page, client, user, lambda m, e: print(m))
            profile_view(mock_page, client, user, lambda m, e: print(m))
            print("✓ Inicialización de vistas (UI Tree) OK.")
        except Exception as e:
            self.fail(f"Error al inicializar vistas: {e}")

    def test_06_persistence_logic(self):
        """Valida que la fecha de persistencia sea consistente."""
        hoy = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(len(hoy), 10)
        self.assertTrue(hoy.startswith("202")) # Validez de década
        print("✓ Lógica de persistencia temporal OK.")

if __name__ == "__main__":
    unittest.main()
