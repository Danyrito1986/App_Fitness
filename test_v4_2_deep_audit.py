import os
from dotenv import load_dotenv
from supabase_config import create_custom_client

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def run_deep_audit():
    """
    Auditoría final sobre los datos de producción para garantizar CERO errores.
    """
    print("\n🕵️‍♂️ INICIANDO AUDITORÍA PROFUNDA V4.2 (Datos de Producción)...")
    
    if not url or not key:
        print("❌ Error: Sin credenciales.")
        return

    try:
        client = create_custom_client(url, key)
        
        # 1. TEST DE CONTEO Y ESTRUCTURA
        # Perfil: Hombre, Intermedio, Masa, Mes 1, Semana 1
        print("📊 Validando estructura del Ciclo de 5 Días...")
        errores = 0
        ejercicios_semana = []

        for dia in range(1, 6):
            res = client.table("ejercicios").select("nombre").eq("mes", 1).eq("semana", 1).eq("dia", dia).eq("genero", "Hombre").eq("nivel", "Intermedio").eq("objetivo", "Aumento de masa muscular").execute()
            
            conteo = len(res.data)
            nombres = [r["nombre"] for r in res.data]
            ejercicios_semana.extend(nombres)
            
            print(f"   Día {dia}: {conteo} ejercicios detectados.")
            if conteo != 6:
                print(f"   ❌ ERROR: El Día {dia} tiene {conteo} ejercicios (Se esperaban 6).")
                errores += 1
            else:
                print(f"   ✅ Día {dia} OK.")

        # 2. TEST DE REDUNDANCIA (Cero Repeticiones)
        print("\n🔍 Buscando redundancias en la rutina semanal...")
        unicos = set(ejercicios_semana)
        if len(unicos) == 30:
            print(f"   ✅ CERO REDUNDANCIA: 30 de 30 ejercicios son únicos.")
        else:
            print(f"   ❌ ERROR: Se detectaron {30 - len(unicos)} ejercicios repetidos.")
            # Identificar repetidos
            vistos = set()
            repetidos = [x for x in ejercicios_semana if x in vistos or vistos.add(x)]
            print(f"   ⚠️  Repetidos: {list(set(repetidos))}")
            errores += 1

        # 3. TEST DE PROGRESIÓN (Semana 1 vs Semana 3)
        print("\n📈 Validando Curva de Intensidad (S1 vs S3)...")
        s1 = client.table("ejercicios").select("reps").eq("mes", 1).eq("semana", 1).eq("dia", 1).limit(1).execute()
        s3 = client.table("ejercicios").select("reps").eq("mes", 1).eq("semana", 3).eq("dia", 1).limit(1).execute()

        if s1.data and s3.data:
            r1 = int(s1.data[0]["reps"])
            r3 = int(s3.data[0]["reps"])
            print(f"   S1 Reps: {r1} | S3 Reps: {r3}")
            if r3 < r1:
                print("   ✅ Progresión de Intensidad: OK (Menos reps, más peso).")
            else:
                print("   ❌ Progresión de Intensidad: FALLÓ.")
                errores += 1

        # RESULTADO FINAL
        print("\n" + "="*40)
        if errores == 0:
            print("✨ RESULTADO: 100% OPERATIVO. SIN ERRORES DETECTADOS.")
        else:
            print(f"💥 RESULTADO: SE DETECTARON {errores} ERRORES CRÍTICOS.")
        print("="*40)

    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    run_deep_audit()
