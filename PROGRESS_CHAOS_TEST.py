import unittest
import flet as ft
from unittest.mock import MagicMock, patch
import db_manager as db
from models import User, PRLog, WeightHistory
from views.progress_view import progress_view
import math

class ProgressChaosTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.session = MagicMock()
        self.mock_page.session.get.return_value = {}
        self.mock_client = MagicMock()
        # Usuario con valores "límite"
        self.user = User(
            id=1, nombre="Chaos User", objetivo="Resistencia", peso_actual=0.0, 
            genero="Mujer", nivel="Avanzado", altura=0, cuello=0, cintura=0, cadera=0, edad=0,
            pecho=0, gluteo=0, bicep=0, muslo=0
        )

    @patch('db_manager.get_weight_history')
    @patch('db_manager.get_prs')
    @patch('db_manager.get_workout_stats')
    def test_01_prs_with_zero_weight(self, mock_stats, mock_prs, mock_history):
        """Simula PRs con peso 0 para intentar romper el escalado de la gráfica de fuerza."""
        print("\n  - Chaos PR: Pesos en cero y nombres de ejercicio vacíos...")
        mock_stats.return_value = 5
        mock_prs.return_value = [
            PRLog(usuario_id=1, ejercicio_nombre="", peso=0.0, fecha="2026-05-01"),
            PRLog(usuario_id=1, ejercicio_nombre=" ", peso=0.0, fecha="2026-05-02")
        ]
        mock_history.return_value = []
        
        try:
            view = progress_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            # Intentar disparar el cambio de dropdown (si existe el control)
            tabs = next(c for c in view.controls if isinstance(c, ft.Tabs))
            fuerza_tab_content = tabs.tabs[1].content
            # Si hay dropdown, lo probamos
            dropdowns = [c for c in fuerza_tab_content.controls if isinstance(c, ft.Dropdown)]
            if dropdowns:
                dd = dropdowns[0]
                mock_event = MagicMock()
                mock_event.control.value = dd.value
                dd.on_change(mock_event)
            print("  [PASSED] Gráfica de fuerza resiliente a valores cero.")
        except Exception as e:
            self.fail(f"Fallo en Tab de Fuerza con datos basura: {e}")

    @patch('db_manager.get_weight_history')
    @patch('db_manager.get_prs')
    @patch('db_manager.get_workout_stats')
    def test_02_composition_with_all_zeros(self, mock_stats, mock_prs, mock_history):
        """Prueba la pestaña de composición con medidas corporales en cero (División por cero en macros)."""
        print("  - Chaos Composition: Medidas en cero (Búsqueda de crash matemático)...")
        mock_stats.return_value = 0
        mock_prs.return_value = []
        mock_history.return_value = []
        
        try:
            view = progress_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            tabs = next(c for c in view.controls if isinstance(c, ft.Tabs))
            comp_tab = tabs.tabs[2].content
            self.assertIsNotNone(comp_tab)
            print("  [PASSED] Pestaña de composición resiliente a medidas nulas.")
        except Exception as e:
            self.fail(f"Fallo catastrófico en Composición por medidas en cero: {e}")

    @patch('db_manager.get_weight_history')
    @patch('db_manager.get_prs')
    def test_03_weight_history_extreme_spikes(self, mock_prs, mock_history):
        """Prueba picos absurdos de peso (ej. de 70kg a 700kg) para validar el renderizado del LineChart."""
        print("  - Chaos Weight: Picos de peso extremos (70kg -> 999kg)...")
        mock_prs.return_value = []
        mock_history.return_value = [
            WeightHistory(usuario_id=1, peso=70.0, fecha="2026-05-01"),
            WeightHistory(usuario_id=1, peso=999.9, fecha="2026-05-02")
        ]
        
        try:
            view = progress_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            self.assertIsNotNone(view)
            print("  [PASSED] Gráfica de peso resiliente a picos de datos absurdos.")
        except Exception as e:
            self.fail(f"La gráfica de peso tronó con picos extremos: {e}")

if __name__ == "__main__":
    print("\n" + "☢️"*15)
    print("INICIANDO CHAOS STRESS TEST: PROGRESS DASHBOARD")
    print("☢️"*15)
    unittest.main(exit=False)
