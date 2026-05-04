import os
from dotenv import load_dotenv
from supabase_config import create_custom_client

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def run_smoke_test():
    """
    Intenta insertar 5 ejercicios de prueba con Mes 99 para validar la conexión y el esquema.
    """
    print("\n🧪 Iniciando SMOKE TEST de Inyección (Prueba y Error)...")
    
    if not url or not key:
        print("❌ Error: No se encontraron credenciales en el .env")
        return

    # 5 Ejercicios de prueba minimalistas
    test_data = [
        {
            "nombre": f"Ejercicio Test {i}",
            "series": 3,
            "reps": 10,
            "descanso": 60,
            "genero": "Hombre",
            "nivel": "Novato",
            "objetivo": "Aumento de masa muscular",
            "mes": 99,  # Mes especial para fácil limpieza
            "semana": 1,
            "dia": 1
        } for i in range(1, 6)
    ]

    try:
        print(f"📡 Conectando a Supabase: {url[:20]}...")
        client = create_custom_client(url, key)
        
        print("🧹 Limpiando cualquier residuo previo del Mes 99...")
        client.table("ejercicios").delete().eq("mes", 99).execute()

        print(f"📤 Intentando insertar {len(test_data)} registros de prueba...")
        response = client.table("ejercicios").insert(test_data).execute()
        
        if response.data:
            print(f"✅ ÉXITO: Se insertaron {len(response.data)} registros correctamente.")
            
            # Verificación de lectura
            print("🔍 Verificando persistencia...")
            check = client.table("ejercicios").select("*").eq("mes", 99).execute()
            if len(check.data) == 5:
                print("💎 Integridad confirmada: Los datos están vivos en la nube.")
                
                # Opcional: Limpiar después del éxito
                print("♻️  Limpiando datos de prueba (Mes 99)...")
                client.table("ejercicios").delete().eq("mes", 99).execute()
                print("✨ Smoke Test Finalizado con 100% de éxito.")
            else:
                print("⚠️  Advertencia: Los datos se insertaron pero la verificación falló.")
        else:
            print("❌ Error: La respuesta de Supabase no contiene datos.")

    except Exception as e:
        print(f"\n💥 ERROR DETECTADO (Prueba y Error):")
        print(f"Tipo: {type(e).__name__}")
        print(f"Detalle: {e}")
        print("\nPosibles causas:")
        print("1. El campo 'descanso' o 'semana' no existe en la tabla remota.")
        print("2. Restricciones de Row Level Security (RLS) impiden la inserción.")
        print("3. Problemas de latencia de red (Timeout).")

if __name__ == "__main__":
    run_smoke_test()
