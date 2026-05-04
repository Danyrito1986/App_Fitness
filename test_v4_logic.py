import unittest
from unittest.mock import MagicMock
from models import User
from views.home_view import home_view
from components.status_header import StatusHeader
import flet as ft

class TestV4PureSplitsLogic(unittest.TestCase):
    def setUp(self):
        self.user = User(
            id=1, nombre="Test User", objetivo="Aumento de masa muscular",
            peso_actual=80.0, entrenos_mes=0, mes_actual=1, nivel="Intermedio"
        )
        self.mock_page = MagicMock()
        self.mock_client = MagicMock()

    def test_home_view_labels(self):
        """Verifica que el Dashboard muestre los nuevos patrones puros según el día."""
        print("\n🔍 Validando etiquetas de Dashboard (INICIO)...")
        
        casos = [
            (0, "Empuje Superior"), # Día 1 (index 0 -> mod 5 + 1 = 1)
            (1, "Jalón Superior"),  # Día 2
            (2, "Empuje Inferior"), # Día 3
            (3, "Jalón Inferior"),  # Día 4
            (4, "Core y Estabilidad") # Día 5
        ]
        
        for entrenos, esperado in casos:
            self.user.entrenos_mes = entrenos
            # Extraer el contenido de la vista (que es una Columna)
            view = home_view(self.mock_page, self.mock_client, self.user, lambda m, e: None, lambda: None)
            
            # El mensaje de músculos está en el Header (primer elemento de la columna)
            header_container = view.controls[0]
            mensaje_text = header_container.content.controls[1].value
            
            self.assertIn(esperado, mensaje_text)
            print(f"  [OK] Entrenos: {entrenos} -> Detectado: {esperado}")

    def test_status_header_dynamic_titles(self):
        """Verifica que el encabezado de entrenamiento cambie el título según el día seleccionado."""
        print("\n🔍 Validando encabezados dinámicos en Entrenamiento...")
        header = StatusHeader(self.user)
        
        casos = [
            (1, "EMPUJE SUPERIOR"),
            (2, "JALÓN SUPERIOR"),
            (3, "EMPUJE INFERIOR"),
            (4, "JALÓN INFERIOR"),
            (5, "CORE")
        ]
        
        for dia, esperado in casos:
            header.update_rutina(1, 1, dia)
            self.assertIn(esperado, header.lbl_rutina_actual.value)
            print(f"  [OK] Día: {dia} -> Título Header: {esperado}")

    def test_week_progression_logic(self):
        """Verifica que la lógica de semanas (S1-S4) sea coherente."""
        print("\n🔍 Validando lógica de Semanas (S1-S4)...")
        
        # Simular 7 entrenos (Día 2 de la Semana 2)
        self.user.entrenos_mes = 7 
        semana_esperada = (7 // 5) % 4 + 1 # (1) % 4 + 1 = 2
        dia_esperado = (7 % 5) + 1 # 2 + 1 = 3
        
        view = home_view(self.mock_page, self.mock_client, self.user, lambda m, e: None, lambda: None)
        header_container = view.controls[0]
        mensaje_text = header_container.content.controls[1].value
        
        self.assertIn(f"Sem {semana_esperada}", mensaje_text)
        self.assertIn(f"Día {dia_esperado}", mensaje_text)
        print(f"  [OK] Progreso: {self.user.entrenos_mes} -> Sem {semana_esperada} - Día {dia_esperado}")

if __name__ == "__main__":
    print("====================================================")
    print("TEST DE LÓGICA V4: PATRONES PUROS Y SEMANAS")
    print("====================================================")
    unittest.main()
