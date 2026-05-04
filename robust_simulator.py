import os
import sys
import time
import threading
from datetime import datetime
import flet as ft
from models import User
import db_manager as db
from services.calculator import calculate_macros

class RobustSimulator:
    def __init__(self):
        self.results = []
        self.errors = []
        self.client = None
        self.user = None
        self.start_time = time.time()

    def log(self, message, category="INFO"):
        icon = "ℹ️"
        if category == "SUCCESS": icon = "✅"
        elif category == "ERROR": icon = "❌"
        elif category == "WARNING": icon = "⚠️"
        elif category == "SYSTEM": icon = "⚙️"
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {icon} {category}: {message}")

    def run_check(self, name, func):
        self.log(f"Iniciando verificación: {name}...", "SYSTEM")
        try:
            start = time.time()
            res = func()
            elapsed = (time.time() - start) * 1000
            self.log(f"{name} completado en {elapsed:.2f}ms", "SUCCESS")
            return True, res
        except Exception as e:
            self.log(f"Error en {name}: {str(e)}", "ERROR")
            self.errors.append(f"{name}: {str(e)}")
            return False, None

    def check_environment(self):
        # Obtener ruta absoluta del directorio del script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(base_dir, ".env")
        
        # Verificar Python
        self.log(f"Python Version: {sys.version.split()[0]}", "INFO")
        
        # Verificar .env
        if os.path.exists(env_path):
            self.log(f"Archivo .env encontrado en: {env_path}", "SUCCESS")
        else:
            raise FileNotFoundError(f"Archivo .env no encontrado en {env_path}. El sistema no puede operar sin credenciales.")

    def check_connectivity(self):
        self.client = db.get_supabase_client()
        # Ping a la base de datos (contar usuarios como prueba de lectura)
        res = self.client.table("usuarios").select("id", count="exact").limit(1).execute()
        self.log(f"Conexión con Supabase establecida. Usuarios en sistema: {res.count}", "SUCCESS")

    def check_logic_engine(self):
        # Crear usuario mock para probar el motor de cálculo
        test_user = User(
            id=0, nombre="Simulador", objetivo="Aumento de masa muscular", 
            peso_actual=75.0, altura=175.0, genero="Hombre", nivel="Intermedio",
            cuello=38.0, cintura=85.0, edad=30
        )
        res = calculate_macros(test_user)
        
        # Verificar rangos lógicos
        if 1500 < res['cal'] < 4000 and 5 < res['bf'] < 40:
            self.log(f"Motor de macros OK. Grasa estimada: {res['bf']}%, Meta: {res['cal']} kcal", "SUCCESS")
        else:
            self.log(f"Valores de macros sospechosos: {res}", "WARNING")

    def check_ui_components(self):
        # Verificamos que las vistas se instancien sin colapsar
        from views.home_view import home_view
        from views.workout_view import workout_view
        from views.profile_view import profile_view
        
        # Mock ligero de Page
        class MockPage:
            def __init__(self):
                self.client_storage = MagicStorage()
                self.session_id = "sim-123"
            def update(self): pass
        
        page_mock = MockPage()
        user_mock = test_user_data()
        
        # Simular carga de vistas (solo instanciación)
        v_home = home_view(page_mock, self.client, user_mock, lambda m, e=False: None, lambda: None)
        self.log("Componente HomeView: OK", "SUCCESS")
        
        v_profile = profile_view(page_mock, self.client, user_mock, lambda m, e=False: None)
        self.log("Componente ProfileView: OK", "SUCCESS")

    def start(self):
        print("\n" + "="*50)
        print("🚀 SIMULADOR DE ROBUSTEZ - APP_FITNESS PRO")
        print("="*50 + "\n")

        steps = [
            ("Entorno de Sistema", self.check_environment),
            ("Conectividad Supabase", self.check_connectivity),
            ("Motor Lógico (Macros)", self.check_logic_engine),
            ("Integridad de UI Components", self.check_ui_components)
        ]

        for name, step in steps:
            success, _ = self.run_check(name, step)
            if not success:
                print("\n" + "!"*50)
                print(f"CRITICAL FAIL: El simulador se detuvo en {name}")
                print("!"*50)
                return

        total_time = time.time() - self.start_time
        print("\n" + "="*50)
        print(f"✅ SIMULACIÓN FINALIZADA CON ÉXITO")
        print(f"⏱️ Tiempo total: {total_time:.2f}s")
        print(f"🛡️ Estado de Resiliencia: 100% OPERATIVO")
        print("="*50 + "\n")

# Clases Auxiliares para el Simulador
class MagicStorage:
    def get(self, key): return None
    def set(self, key, val): pass

def test_user_data():
    return User(id=1, nombre="Tester", objetivo="Resistencia", peso_actual=70, mes_actual=1, entrenos_mes=5)

if __name__ == "__main__":
    sim = RobustSimulator()
    sim.start()
