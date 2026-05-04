import os
from dotenv import load_dotenv
from supabase_config import create_custom_client
from seed_v4_pure_splits import seed_pure_splits_v4

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def run_logic_test():
    """
    Toma una muestra real de la biblioteca V4 y valida la lógica de progresión en la nube.
    """
    print("\n🧪 Iniciando TEST DE VALIDACIÓN LÓGICA (Datos Reales)...")
    
    # 1. Obtener todos los ejercicios generados (sin insertar aún)
    todos_los_ejercicios = seed_pure_splits_v4(execute_insert=False)
    
    # 2. Filtrar una muestra: Hombre, Novato, Aumento de masa muscular (Mes 1)
    # Cambiaremos el mes a 98 para la prueba
    muestra = [
        ex.copy() for ex in todos_los_ejercicios 
        if ex["genero"] == "Hombre" and ex["nivel"] == "Novato" and ex["objetivo"] == "Aumento de masa muscular"
    ]
    
    for ex in muestra:
        ex["mes"] = 98 # Mes de prueba

    print(f"📦 Muestra seleccionada: {len(muestra)} ejercicios (Ciclo completo 4 semanas).")

    try:
        client = create_custom_client(url, key)
        
        print("🧹 Limpiando Mes 98...")
        client.table("ejercicios").delete().eq("mes", 98).execute()

        print("📤 Subiendo muestra a Supabase...")
        client.table("ejercicios").insert(muestra).execute()

        # 3. VERIFICACIÓN DE LÓGICA DE PROGRESIÓN
        print("\n🔍 Validando Progresión de Carga en la nube:")
        
        # Consultar Semana 1 vs Semana 2 del primer ejercicio (Press de Banca)
        res_s1 = client.table("ejercicios").select("*").eq("mes", 98).eq("semana", 1).eq("dia", 1).limit(1).execute()
        res_s2 = client.table("ejercicios").select("*").eq("mes", 98).eq("semana", 2).eq("dia", 1).limit(1).execute()

        if res_s1.data and res_s2.data:
            ex1 = res_s1.data[0]
            ex2 = res_s2.data[0]
            
            print(f"📊 {ex1['nombre']}:")
            print(f"   Semana 1: {ex1['series']} series, {ex1['reps']} reps")
            print(f"   Semana 2: {ex2['series']} series, {ex2['reps']} reps")
            
            if ex2['series'] > ex1['series']:
                print("✅ LÓGICA DE VOLUMEN: OK (S2 tiene más series que S1)")
            else:
                print("❌ LÓGICA DE VOLUMEN: FALLÓ")
        
        # 4. Limpiar después de validar
        print("\n♻️  Limpiando Mes 98...")
        client.table("ejercicios").delete().eq("mes", 98).execute()
        print("✨ Test de Validación Lógica finalizado con éxito.")

    except Exception as e:
        print(f"❌ Error durante el test: {e}")

if __name__ == "__main__":
    # Importante: seed_pure_splits_v4 devuelve la lista si execute_insert=False
    # Pero debemos asegurarnos de que la función retorne la lista de ejercicios.
    # Re-importando para asegurar
    from seed_v4_pure_splits import seed_pure_splits_v4 as get_data
    run_logic_test()
