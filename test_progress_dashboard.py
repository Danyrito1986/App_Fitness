import unittest
from unittest.mock import MagicMock, patch
import flet as ft
from views.progress_view import progress_view
from models import User, PRLog, WeightHistory

class TestProgressDashboard(unittest.TestCase):
    def setUp(self):
        self.user = User(
            id=1, nombre="Test User", objetivo="Resistencia", 
            peso_actual=75.0, genero="Hombre", nivel="Novato",
            altura=175, cuello=38, cintura=80, cadera=90, edad=25,
            pecho=95, gluteo=90, bicep=33, muslo=50,
            mes_actual=1, entrenos_mes=0
        )
        self.page = MagicMock(spec=ft.Page)
        self.page.session = MagicMock()
        self.page.session.get.return_value = {}
        self.client = MagicMock()

    @patch('db_manager.get_weight_history')
    @patch('db_manager.get_prs')
    @patch('db_manager.get_workout_stats')
    def test_rendering_with_data(self, mock_stats, mock_prs, mock_history):
        """Verifica que el dashboard renderice todas las pestañas con datos."""
        mock_stats.return_value = 10
        mock_prs.return_value = [
            PRLog(usuario_id=1, ejercicio_nombre="Press Banca", peso=60, fecha="2026-05-01"),
            PRLog(usuario_id=1, ejercicio_nombre="Press Banca", peso=65, fecha="2026-05-06")
        ]
        mock_history.return_value = [
            WeightHistory(usuario_id=1, peso=76, fecha="2026-05-01"),
            WeightHistory(usuario_id=1, peso=75, fecha="2026-05-06")
        ]

        view = progress_view(self.page, self.client, self.user, lambda m, e: None)
        
        self.assertIsInstance(view, ft.Column)
        # Buscar el componente ft.Tabs
        tabs_control = next((c for c in view.controls if isinstance(c, ft.Tabs)), None)
        self.assertIsNotNone(tabs_control)
        self.assertEqual(len(tabs_control.tabs), 3)
        print("✅ Dashboard renderizado con 3 pestañas: OK")

    @patch('db_manager.get_weight_history')
    @patch('db_manager.get_prs')
    @patch('db_manager.get_workout_stats')
    def test_rendering_empty(self, mock_stats, mock_prs, mock_history):
        """Verifica resiliencia cuando no hay datos."""
        mock_stats.return_value = 0
        mock_prs.return_value = []
        mock_history.return_value = []

        view = progress_view(self.page, self.client, self.user, lambda m, e: None)
        self.assertIsInstance(view, ft.Column)
        print("✅ Dashboard resiliente a falta de datos: OK")

if __name__ == "__main__":
    unittest.main()
