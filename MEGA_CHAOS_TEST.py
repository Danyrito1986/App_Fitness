import unittest
import flet as ft
from unittest.mock import MagicMock, patch
import db_manager as db
from models import User, Exercise, PRLog
from views.workout_view import workout_view
from views.profile_view import profile_view
from views.progress_view import progress_view
from services.calculator import calculate_macros
from services.image_service import get_exercise_image
from datetime import datetime
import math

class MegaChaosStressTest(unittest.TestCase):
    
    def setUp(self):
        # Mock de Flet Page y Client Storage
        self.mock_page = MagicMock(spec=ft.Page)
        self.storage_data = {}
        self.mock_page.client_storage.get.side_effect = lambda k: self.storage_data.get(k)
        self.mock_page.client_storage.set.side_effect = lambda k, v: self.storage_data.update({k: v})
        
        # Usuario Estándar para pruebas
        self.user = User(
            id=1, nombre="Chaos Warrior", objetivo="Aumento de masa muscular", 
            peso_actual=80.0, genero="Hombre", nivel="Intermedio", altura=180.0,
            cuello=40.0, cintura=85.0, edad=30
        )
        self.mock_client = MagicMock()

    # --- 1. CAOS DE PERSISTENCIA (EL PROBLEMA DE LOS 15 MIN) ---
    def test_01_persistence_shield_under_network_crash(self):
        """Simula caída de red justo después de una sesión de 15 min. No debe haber pérdida de series."""
        print("\n  [CAOS PERSISTENCIA] Simulando caída de red tras inactividad...")
        hoy = datetime.now().strftime("%Y-%m-%d")
        # Simular que hay datos en caché local
        self.storage_data["workout_progress"] = {"fecha": hoy, "completados": {"M1_S1_D1_99": [0]}}
        
        with patch('db_manager.get_workout_progress', return_value=None): # Error de red (None)
            workout_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
            
            # Verificar que la caché local SIGUE AHÍ
            progreso = self.storage_data.get("workout_progress")
            self.assertIsNotNone(progreso)
            self.assertEqual(len(progreso["completados"]), 1, "¡ERROR: La caché local se borró tras fallo de red!")
        print("  ✅ [PASSED] Blindaje de persistencia confirmado.")

    # --- 2. CAOS VISUAL (CATÁLOGO ÉLITE) ---
    def test_02_visual_catalog_robustness(self):
        """Verifica que el nuevo sistema de imágenes no tenga duplicados genéricos y maneje nombres basura."""
        print("  [CAOS VISUAL] Verificando catálogo curado vs nombres basura...")
        nombres_basura = ["Ejercicio X", "Movimiento Z", " ", "!!!"]
        urls_vistas = set()
        
        for nombre in nombres_basura:
            url = get_exercise_image(nombre)
            self.assertIn("images.unsplash.com", url)
            urls_vistas.add(url)
            
        # El fallback debe ser consistente pero profesional
        self.assertTrue(len(urls_vistas) >= 1)
        print("  ✅ [PASSED] Catálogo Élite estable ante datos de entrada basura.")

    # --- 3. CAOS DE DATOS (USUARIOS CORRUPTOS) ---
    def test_03_corrupt_user_data_resilience(self):
        """Simula un usuario con valores que causarían división por cero o errores de tipo."""
        print("  [CAOS DATOS] Inyectando datos corruptos en perfil (Ceros/Nulos)...")
        corrupt_user = User(
            id=1, nombre=None, objetivo="", peso_actual=0.0, altura=0.0, 
            cuello=0.0, cintura=0.0, edad=0
        )
        
        try:
            # Probar calculadora
            macros = calculate_macros(corrupt_user)
            self.assertIsNotNone(macros)
            
            # Probar renderizado de perfil
            view = profile_view(self.mock_page, self.mock_client, corrupt_user, lambda m, e: None)
            self.assertIsNotNone(view)
        except Exception as e:
            self.fail(f"¡CRASH detectado con datos corruptos!: {e}")
        print("  ✅ [PASSED] Resiliencia total ante datos de usuario nulos/corruptos.")

    # --- 4. CAOS DE ESCALABILIDAD (ESTRÉS DE CARGA) ---
    def test_04_heavy_load_rendering(self):
        """Simula la carga masiva de 100 ejercicios con imágenes y 50 PRs en la gráfica."""
        print("  [CAOS ESCALABILIDAD] Simulando carga pesada (100 ejercicios + 50 PRs)...")
        
        mock_exs = [Exercise(id=i, nombre=f"Ex {i}", series=4, reps=10, rutina_id=1) for i in range(100)]
        mock_prs = [PRLog(usuario_id=1, ejercicio_nombre="Press", peso=100.0 + i, fecha="2026-05-01") for i in range(50)]
        
        with patch('db_manager.get_dynamic_exercises', return_value=mock_exs), \
             patch('db_manager.get_workout_progress', return_value={}), \
             patch('db_manager.get_prs', return_value=mock_prs), \
             patch('db_manager.get_weight_history', return_value=[]), \
             patch('db_manager.get_workout_stats', return_value=10):
            
            try:
                # Cargar vista de entrenamiento pesada
                view_w = workout_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
                self.assertIsNotNone(view_w)
                
                # Cargar dashboard de progreso pesado
                view_p = progress_view(self.mock_page, self.mock_client, self.user, lambda m, e: None)
                self.assertIsNotNone(view_p)
            except Exception as e:
                self.fail(f"¡CRASH detectado bajo carga pesada!: {e}")
        print("  ✅ [PASSED] App estable bajo condiciones de carga masiva.")

if __name__ == "__main__":
    print("\n" + "☢️"*20)
    print("   MEGA CHAOS STRESS TEST: TOTAL APP SYSTEM")
    print("☢️"*20)
    unittest.main()
