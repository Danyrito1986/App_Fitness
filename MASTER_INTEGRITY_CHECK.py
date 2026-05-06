import os
import sys
import unittest
import flet as ft
from unittest.mock import MagicMock
import db_manager as db
from models import User

class MasterIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*50)
        print("🚀 INICIANDO MASTER INTEGRITY CHECK - APP_FITNESS")
        print("="*50)
        cls.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        cls.client = db.get_supabase_client()
        cls.user = User(
            id=1, nombre="Test Admin", objetivo="Aumento de masa muscular", 
            peso_actual=80.0, genero="Hombre", nivel="Intermedio",
            altura=180, cuello=40, cintura=85, cadera=90, edad=30,
            mes_actual=1, entrenos_mes=5
        )

    def test_01_supabase_connectivity(self):
        """1. Validar conexión y respuesta de Supabase."""
        try:
            res = self.client.table("usuarios").select("count", count="exact").limit(1).execute()
            self.assertIsNotNone(res.count)
            print("  [OK] Conexión Supabase: Estable")
        except Exception as e:
            self.fail(f"Fallo de conexión a Supabase: {e}")

    def test_02_exercise_database_integrity(self):
        """2. Validar conteo total de ejercicios (Debe ser 4320)."""
        res = self.client.table("ejercicios").select("id", count="exact").execute()
        total = res.count
        self.assertEqual(total, 4320, f"Inconsistencia en DB: Se esperaban 4320 ejercicios, se encontraron {total}")
        print(f"  [OK] Integridad de DB Ejercicios: {total} registros detectados")

    def test_03_diet_json_integrity(self):
        """3. Validar archivo de datos de dieta."""
        json_path = os.path.join(self.BASE_DIR, "assets", "data", "diet_plan.json")
        self.assertTrue(os.path.exists(json_path), f"Falta el archivo diet_plan.json en {json_path}")
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("fuentes", data)
            self.assertIn("matriz", data)
        print("  [OK] Integridad Diet JSON: Válido")

    def test_04_profile_ui_structure(self):
        """4. Validar que el rediseño del perfil no tenga errores de iconos o anchos."""
        from views.profile_view import profile_view
        mock_page = MagicMock(spec=ft.Page)
        mock_page.session = MagicMock()
        mock_page.session.get.return_value = {}
        try:
            view = profile_view(mock_page, self.client, self.user, lambda m, e: None)
            # Verificar Card de datos personales
            self.assertIsInstance(view.controls[2], ft.Card)
            # Verificar ExpansionTile
            self.assertIsInstance(view.controls[4], ft.ExpansionTile)
            print("  [OK] Estructura UI Perfil: Verificada")
        except Exception as e:
            self.fail(f"Error de UI en Perfil: {e}")

    def test_05_workout_logic_persistence(self):
        """5. Validar lógica de guardado rápido (0.1s)."""
        view_path = os.path.join(self.BASE_DIR, "views", "workout_view.py")
        import threading
        # Buscamos el valor de timer en el código fuente de la vista
        with open(view_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("threading.Timer(0.1, persistir_nube)", content)
        print("  [OK] Lógica de Persistencia Rápida: Confirmada")

    def test_06_deployment_config(self):
        """6. Validar Procfile y requirements.txt."""
        proc_path = os.path.join(self.BASE_DIR, "Procfile")
        req_path = os.path.join(self.BASE_DIR, "requirements.txt")
        
        with open(proc_path, "r") as f:
            self.assertIn("python app_fitness.py", f.read())
        with open(req_path, "r") as f:
            reqs = f.read()
            self.assertIn("flet", reqs)
            self.assertIn("supabase", reqs)
        print("  [OK] Configuración de Despliegue: Correcta")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MasterIntegrityTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n" + "✨"*15)
        print("SISTEMA 100% ÍNTEGRO")
        print("LISTO PARA PRODUCCIÓN")
        print("✨"*15 + "\n")
    else:
        sys.exit(1)
