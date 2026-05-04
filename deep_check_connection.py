import os
import db_manager as db
from dotenv import load_dotenv
import httpx
import time

def deep_analyze_connection():
    print("=== ANÁLISIS PROFUNDO DE CONEXIÓN (SUPABASE) ===")
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("[CRÍTICO] Variables de entorno faltantes.")
        return

    # 1. Prueba de Ping DNS con httpx directo (sin conflicto de nombre)
    print("\n1. Probando resolución DNS y conectividad básica...")
    try:
        with httpx.Client() as client_test:
            response = client_test.get(url, timeout=5.0)
            print(f"[OK] Servidor responde. Status: {response.status_code}")
    except Exception as e:
        print(f"[FALLO] Error de red básico: {e}")

    # 2. Prueba de Cliente Supabase
    print("\n2. Probando inicialización de cliente Supabase...")
    try:
        client = db.get_supabase_client()
        # Intentar obtener el usuario actual (auth)
        auth_user = client.auth.get_user()
        print(f"[OK] Auth check exitoso. Sesión: {'Activa' if auth_user else 'Vacía'}")
        
        # Prueba de tabla usuarios
        res = client.table("usuarios").select("count", count="exact").execute()
        print(f"[OK] DB Check exitoso. Filas en usuarios: {res.count}")
    except Exception as e:
        print(f"[FALLO] Error en cliente Supabase: {e}")

if __name__ == "__main__":
    deep_analyze_connection()
