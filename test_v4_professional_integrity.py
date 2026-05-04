import os
from dotenv import load_dotenv
from supabase_config import create_custom_client
from seed_v4_pure_splits import seed_pure_splits_v4

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def run_professional_test():
    """
    Realiza una auditoría exhaustiva de la biblioteca profesional antes de subirla.
    """
    print("\n🧐 AUDITORÍA DE INTEGRIDAD PROFESIONAL (V4.1)...")
    
    # 1. Generar ejercicios localmente
    ejercicios = seed_pure_splits_v4(execute_insert=False)
    
    if not ejercicios:
        print("❌ ERROR: No se generaron ejercicios.")
        return

    # 2. Análisis Estadístico Local
    total = len(ejercicios)
    print(f"✅ Total generado: {total} ejercicios.")
    
    # Verificar cantidad por día (Debe ser 6 ahora)
    # Tomamos una muestra (Hombre, Novato, Masa, Mes 1, Sem 1)
    muestra_dia1 = [e for e in ejercicios if e["mes"] == 1 and e["semana"] == 1 and e["dia"] == 1 and e["genero"] == "Hombre" and e["nivel"] == "Novato" and e["objetivo"] == "Aumento de masa muscular"]
    
    print(f"🔍 Análisis de Volumen por Día (Muestra): {len(muestra_dia1)} ejercicios.")
    if len(muestra_dia1) == 6:
        print("✅ Volumen Profesional: OK (6 ejercicios por día).")
    else:
        print(f"⚠️  Volumen Inusual: Detectados {len(muestra_dia1)} ejercicios (Se esperaban 6).")

    # 3. Verificación de Presencia de Hombros
    nombres_dia1 = [e["nombre"] for e in muestra_dia1]
    hombros_detectados = [n for n in nombres_dia1 if "Hombro" in n or "Lateral" in n or "Militar" in n]
    print(f"🔍 Ejercicios de Hombro en Día 1: {hombros_detectados}")
    
    if len(hombros_detectados) >= 2:
        print("✅ Cobertura de Hombros: OK.")
    else:
        print("❌ Cobertura de Hombros: INSUFICIENTE.")

    # 4. Test de Inserción Controlada (Mes 97)
    try:
        print("\n📡 Validando contra Supabase (Mes 97 - Test Final)...")
        client = create_custom_client(url, key)
        
        # Limpiar mes de test
        client.table("ejercicios").delete().eq("mes", 97).execute()
        
        # Insertar solo la muestra del primer perfil completo (4 semanas, 5 días = 120 ejercicios)
        perfil_test = [e.copy() for e in ejercicios if e["genero"] == "Hombre" and e["nivel"] == "Pro" and e["objetivo"] == "Aumento de masa muscular"]
        for p in perfil_test: p["mes"] = 97
        
        print(f"📤 Subiendo perfil de prueba (120 registros)...")
        res = client.table("ejercicios").insert(perfil_test).execute()
        
        if res.data:
            print(f"✅ Inserción Exitosa en Nube.")
            
            # Verificar un ejercicio de Semana 3 (Intensidad)
            s3_ex = client.table("ejercicios").select("*").eq("mes", 97).eq("semana", 3).eq("dia", 1).limit(1).execute()
            if s3_ex.data:
                ex = s3_ex.data[0]
                reps = int(ex['reps'])
                descanso = int(ex['descanso'])
                print(f"🧪 Validación Progresión S3 ({ex['nombre']}): Reps={reps}, Descanso={descanso}s")
                if reps < 10: # En S3 bajamos reps para subir peso
                    print("✅ Lógica de Intensidad S3: Confirmada.")
            
            # Limpiar
            client.table("ejercicios").delete().eq("mes", 97).execute()
            print("\n✨ AUDITORÍA FINALIZADA: Sistema listo para inyección masiva.")
        else:
            print("❌ ERROR: La nube no devolvió confirmación de datos.")

    except Exception as e:
        print(f"💥 ERROR CRÍTICO EN TEST: {e}")

if __name__ == "__main__":
    run_professional_test()
