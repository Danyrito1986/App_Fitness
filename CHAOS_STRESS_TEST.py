import unittest
import flet as ft
from unittest.mock import MagicMock, patch
import db_manager as db
from models import User
from views.profile_view import profile_view
from views.workout_view import workout_view
from views.diet_view import diet_view
from services.calculator import calculate_macros
import math

class ChaosStressTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.session = MagicMock()
        self.mock_page.session.get.return_value = {}
        self.mock_page.overlay = []
        self.mock_client = MagicMock()
        self.user = User(
            id=1, nombre="Stress Test", objetivo="Resistencia", peso_actual=70, 
            genero="Hombre", nivel="Novato", altura=170, cuello=35, cintura=80, cadera=90, edad=25
        )

    def test_01_math_robustness_extreme_values(self):
        """Prueba de estrés a las fórmulas matemáticas con valores extremos (Chaos Math)."""
        print("\n  - Probando valores extremos en calculadora...")
        extreme_users = [
            {"peso": 500, "altura": 250, "cintura": 200, "cuello": 10}, # Obesidad extrema
            {"peso": 30, "altura": 100, "cintura": 40, "cuello": 40},   # Desnutrición extrema
            {"peso": 0, "altura": 0, "cintura": 0, "cuello": 0},       # Valores cero (División por cero)
            {"peso": -80, "altura": -180, "cintura": -100, "cuello": -30} # Valores negativos
        ]
        
        for u_data in extreme_users:
            u = User(id=1, nombre="X", objetivo="Masa", peso_actual=u_data['peso'], 
                     genero="Hombre", altura=u_data['altura'], cintura=u_data['cintura'], 
                     cuello=u_data['cuello'], edad=25)
            try:
                res = calculate_macros(u)
                self.assertIsNotNone(res['cal'])
                self.assertFalse(math.isnan(res['cal']), "Resultado NaN detectado")
            except Exception as e:
                self.fail(f"La calculadora tronó con valores {u_data}: {e}")
        print("  [PASSED] Calculadora blindada contra divisiones por cero y valores absurdos.")

    def test_02_ui_resilience_missing_data(self):
        """Prueba de renderizado con datos corruptos o faltantes en el Perfil."""
        print("  - Probando resiliencia de la UI del Perfil...")
        # Forzar datos corruptos en el objeto user
        self.user.nombre = None
        self.user.peso_actual = "Corrupto" # Tipo de dato erróneo
        
        try:
            view = profile_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            self.assertIsInstance(view, ft.Column)
        except Exception as e:
            self.fail(f"La UI de Perfil falló catastróficamente con datos corruptos: {e}")
        print("  [PASSED] UI de Perfil resiliente a datos corruptos.")

    def test_03_db_handshake_timeout_simulation(self):
        """Simula un fallo total de respuesta de Supabase durante la carga de ejercicios."""
        print("  - Simulando 'Database Down' en Entrenamiento...")
        with patch('db_manager.get_dynamic_exercises') as mock_db:
            mock_page = MagicMock(spec=ft.Page)
            mock_db.side_effect = Exception("Supabase Connection Timeout")
            
            try:
                # La vista no debe tronar, debe mostrar un mensaje de error amigable
                view = workout_view(mock_page, self.mock_client, self.user, lambda m, e: None)
                self.assertIsInstance(view, ft.Stack)
            except Exception as e:
                self.fail(f"La vista de entrenamiento tronó al fallar la DB: {e}")
        print("  [PASSED] Manejo de errores de conexión (Workout View).")

    def test_04_diet_interchange_collision(self):
        """Simula intercambios de alimentos contradictorios."""
        print("  - Probando estabilidad de sesión en Dieta...")
        # Simular que el JSON tiene un alimento con densidad 0 (Error humano en carga de datos)
        with patch('json.load') as mock_json:
            mock_json.return_value = {
                "fuentes": {"proteina": [{"nombre": "Veneno", "p": 0, "icon": "info"}]},
                "matriz": {"0": {"Desayuno": {"p": 0, "c": 0, "g": 0}}}
            }
            try:
                # No debe haber crash de división por cero
                view = diet_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
                self.assertIsNotNone(view)
            except Exception as e:
                self.fail(f"La vista de dieta falló con datos de JSON inválidos: {e}")
        print("  [PASSED] Lógica de intercambio blindada contra datos JSON corruptos.")

if __name__ == "__main__":
    print("\n" + "🔥"*15)
    print("INICIANDO CHAOS STRESS TEST (NIVEL CRÍTICO)")
    print("🔥"*15)
    unittest.main(exit=False)
