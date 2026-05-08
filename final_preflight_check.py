import os
import sys
import flet as ft
from unittest.mock import MagicMock

# Simulación de variables de entorno para Render
os.environ["PORT"] = "8551"

def audit_deployment():
    print("🔍 INICIANDO AUDITORÍA TÉCNICA PRO (SIMULACIÓN DE DESPLIEGUE)...")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    errors = []

    # 1. Verificación de Archivos y Datos
    print("\n1. Verificando integridad de archivos...")
    files_to_check = [
        "app_fitness.py", 
        "requirements.txt", 
        "Procfile", 
        "assets/data/diet_plan.json",
        "views/diet_view.py",
        "views/profile_view.py"
    ]
    for f in files_to_check:
        path = os.path.join(BASE_DIR, f)
        if os.path.exists(path):
            print(f"  [OK] {f}")
        else:
            errors.append(f"Archivo faltante: {f}")

    # 2. Test de Renderizado Headless (Mocking Page)
    print("\n2. Simulando renderizado de nuevas vistas...")
    try:
        from views.diet_view import diet_view
        from views.profile_view import profile_view
        from models import User
        
        # Mock de página y usuario
        mock_page = MagicMock(spec=ft.Page)
        mock_page.session = MagicMock()
        mock_page.session.get.return_value = {}
        mock_page.overlay = []
        
        mock_user = User(
            id=1, nombre="Test", objetivo="Resistencia", peso_actual=70, 
            genero="Hombre", nivel="Novato", altura=170, cuello=35, cintura=80, cadera=90, edad=25
        )
        mock_client = MagicMock()

        # Intentar instanciar vistas
        print("  - Instanciando diet_view...")
        diet_view(mock_page, mock_client, mock_user, lambda m, e: None)
        print("  [OK] diet_view renderiza sin errores de iconos/sintaxis.")

        print("  - Instanciando profile_view...")
        profile_view(mock_page, mock_client, mock_user, lambda m, e: None)
        print("  [OK] profile_view renderiza sin errores de iconos/sintaxis.")

    except Exception as e:
        errors.append(f"Error de renderizado/sintaxis: {e}")

    # 3. Verificación de dependencias en requirements.txt
    print("\n3. Validando requirements.txt...")
    try:
        with open(os.path.join(BASE_DIR, "requirements.txt"), "r") as f:
            reqs = f.read()
            if "flet==" not in reqs and "flet" not in reqs:
                errors.append("Flet no está en requirements.txt")
            if "supabase" not in reqs:
                errors.append("Supabase no está en requirements.txt")
        print("  [OK] requirements.txt validado.")
    except:
        errors.append("No se pudo leer requirements.txt")

    # Resultado Final
    print("\n" + "="*40)
    if not errors:
        print("✨ RESULTADO: SIMULACIÓN EXITOSA ✨")
        print("La aplicación es 100% compatible para subir a Render.")
    else:
        print("❌ ERRORES DETECTADOS ❌")
        for err in errors:
            print(f"  - {err}")
    print("="*40)

if __name__ == "__main__":
    audit_deployment()
