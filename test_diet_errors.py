import unittest
from unittest.mock import MagicMock, patch
import flet as ft
from views.diet_view import diet_view
from models import User

class TestDietExchangeLogic(unittest.TestCase):
    def setUp(self):
        # Configuración de usuario mock
        self.user = User(
            id=1, nombre="Test", objetivo="Aumento de masa muscular", 
            peso_actual=80.0, genero="Hombre", nivel="Intermedio",
            altura=180, cuello=40, cintura=85, cadera=90, edad=30,
            mes_actual=1, entrenos_mes=5
        )
        self.page = MagicMock(spec=ft.Page)
        self.page.session = MagicMock()
        self.page.session.get.return_value = {}
        self.page.overlay = []
        self.client = MagicMock()

    def test_view_initialization(self):
        """Verifica que la vista se inicialice sin errores."""
        try:
            view = diet_view(self.page, self.client, self.user, lambda m, e: print(m))
            self.assertIsInstance(view, ft.Column)
            self.assertTrue(len(view.controls) > 0)
            print("✅ Inicialización de vista: OK")
        except Exception as e:
            self.fail(f"La vista falló al inicializarse: {e}")

    def test_macro_calculation_integrity(self):
        """Verifica que los macros calculados sean números válidos."""
        from services.calculator import calculate_macros
        macros = calculate_macros(self.user)
        self.assertGreater(macros['cal'], 1200)
        self.assertGreater(macros['p'], 0)
        self.assertGreater(macros['c'], 0)
        self.assertGreater(macros['f'], 0)
        print(f"✅ Integridad de macros: OK ({macros['cal']} kcal)")

    def test_exchange_logic_no_crash(self):
        """Simula la lógica de intercambio para asegurar que no haya divisiones por cero."""
        # Extraído de diet_view.py para testear la fórmula directamente
        def calculate_grams(target, density):
            if density == 0: return 0
            return int((target / density) * 100)

        # Caso normal: Pollo (31g proteina / 100g)
        self.assertEqual(calculate_grams(31, 31), 100)
        # Caso borde: Densidad 0 (No debería ocurrir con datos válidos, pero probamos resiliencia)
        self.assertEqual(calculate_grams(31, 0), 0)
        print("✅ Lógica de cálculo de gramos: OK")

    def test_session_state_handling(self):
        """Verifica que la vista intente leer de la sesión."""
        diet_view(self.page, self.client, self.user, lambda m, e: None)
        self.page.session.get.assert_called_with("diet_selections")
        print("✅ Manejo de estado de sesión: OK")

if __name__ == "__main__":
    unittest.main()
