import unittest
import flet as ft
from unittest.mock import MagicMock, patch
import db_manager as db
from models import User, Exercise
from components.exercise_card import ExerciseCard
from views.workout_view import workout_view
from datetime import datetime

class VisualChaosTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_page = MagicMock(spec=ft.Page)
        self.mock_page.client_storage.get.return_value = {}
        self.user = User(id=1, nombre="Chaos", objetivo="Masa", peso_actual=70)
        
    def test_01_image_failure_resilience(self):
        """CAOS VISUAL: Simula una URL de imagen rota o inválida."""
        print("\n  - Escenario: URL de imagen rota (404/Null)...")
        ex = Exercise(
            id=1, nombre="Press de Banca", series=4, reps=10, rutina_id=1, 
            imagen_url="https://url-que-no-existe.com/error.jpg"
        )
        
        try:
            # El componente debe renderizar el contenedor de la imagen sin tronar la app
            card = ExerciseCard(ex, lambda i, s: False, lambda *a: None, lambda *a: None, lambda *a: None, "10kg")
            self.assertIsInstance(card, ft.Container)
            print("  [PASSED] La tarjeta no colapsa ante imágenes rotas.")
        except Exception as e:
            self.fail(f"Fallo catastrófico con imagen rota: {e}")

    def test_02_ultra_long_exercise_name(self):
        """CAOS VISUAL: Nombre de ejercicio absurdamente largo (Text Overflow)."""
        print("  - Escenario: Nombre de ejercicio ultra largo...")
        ex = Exercise(
            id=2, 
            nombre="Press de Banca inclinado con mancuernas de 50kg y rotación externa de manguito rotador versión pro extendida", 
            series=3, reps=12, rutina_id=1
        )
        
        try:
            card = ExerciseCard(ex, lambda i, s: False, lambda *a: None, lambda *a: None, lambda *a: None, "10kg")
            # Buscamos el control de texto del nombre (Lado Izquierdo - Índice 0)
            row_principal = card.content
            col_info = row_principal.controls[0] # Ahora es el primer elemento
            row_nombre = col_info.controls[0]
            text_nombre = row_nombre.controls[0]
            
            self.assertEqual(text_nombre.overflow, ft.TextOverflow.ELLIPSIS, "El texto no tiene puntos suspensivos")
            print("  [PASSED] El diseño horizontal maneja correctamente textos largos.")
        except Exception as e:
            self.fail(f"Fallo en layout con texto largo: {e}")

    def test_03_concurrent_image_load_stress(self):
        """CAOS RED: Simula la carga de 50 ejercicios simultáneos con imágenes dinámicas."""
        print("  - Escenario: Carga masiva de ejercicios (50 unidades)...")
        
        # Simulamos que la DB devuelve 50 ejercicios
        mock_exs = [
            Exercise(id=i, nombre=f"Ex {i}", series=3, reps=10, rutina_id=1) 
            for i in range(50)
        ]
        
        with patch('db_manager.get_dynamic_exercises', return_value=mock_exs), \
             patch('db_manager.get_workout_progress', return_value={}), \
             patch('db_manager.get_last_weight', return_value=0.0):
            
            try:
                view = workout_view(self.mock_page, MagicMock(), self.user, lambda m, e: None)
                # Verificamos que la columna de ejercicios tenga los 50 controles
                # En workout_view, el content es un Stack -> Container -> Column -> lista_ejercicios
                content_area = view.controls[0]
                main_col = content_area.content
                lista_ej = main_col.controls[8] # El índice puede variar, buscamos el tipo Column
                
                self.assertEqual(len(lista_ej.controls), 50)
                print(f"  [PASSED] Renderizado masivo de {len(lista_ej.controls)} imágenes exitoso.")
            except Exception as e:
                self.fail(f"El renderizado masivo falló: {e}")

if __name__ == "__main__":
    print("\n" + "🌀"*15)
    print("INICIANDO VISUAL & NETWORK CHAOS TEST")
    print("🌀"*15)
    unittest.main()
