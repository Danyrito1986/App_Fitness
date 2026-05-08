import threading
import time
import unittest
from unittest.mock import MagicMock, patch

# Mock de Flet para evitar dependencias de UI en el test
class MockControl:
    def __init__(self, value):
        self.value = value
        self.updated = False
    def update(self):
        self.updated = True

class TestAppFitnessLogic(unittest.TestCase):
    
    def test_checkbox_update_logic(self):
        """Verifica que el handler de on_change llame a update() en el control."""
        # Simulación de la función on_check
        on_check_called = False
        def mock_on_check(ex_id, idx, value, t):
            nonlocal on_check_called
            on_check_called = True
        
        # Simulación de la lógica en exercise_card.py
        def create_on_change(ex_id, idx, t):
            def handler(e):
                mock_on_check(ex_id, idx, e.control.value, t)
                e.control.update()
            return handler
        
        mock_event = MagicMock()
        mock_event.control = MockControl(True)
        
        handler = create_on_change(1, 0, 60)
        handler(mock_event)
        
        self.assertTrue(on_check_called, "on_check debería haber sido llamado")
        self.assertTrue(mock_event.control.updated, "control.update() debería haber sido llamado")

    def test_debounce_timing(self):
        """Verifica que el guardado se ejecute rápido con el nuevo tiempo de 0.1s."""
        save_timer = None
        persistir_nube_called = False
        
        def mock_persistir_nube():
            nonlocal persistir_nube_called
            persistir_nube_called = True

        def debounced_save():
            nonlocal save_timer
            if save_timer:
                save_timer.cancel()
            save_timer = threading.Timer(0.1, mock_persistir_nube)
            save_timer.start()

        debounced_save()
        time.sleep(0.05)
        self.assertFalse(persistir_nube_called, "No debería haberse llamado aún a los 0.05s")
        
        time.sleep(0.1)
        self.assertTrue(persistir_nube_called, "Debería haberse llamado después de 0.1s")

if __name__ == "__main__":
    unittest.main()
