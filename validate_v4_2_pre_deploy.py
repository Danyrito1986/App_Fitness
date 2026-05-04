import os
from dotenv import load_dotenv
from supabase_config import create_custom_client
from seed_v4_pure_splits import seed_pure_splits_v4

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def run_pre_deploy_validation():
    """
    Simula el despliegue completo en el Mes 96 para detectar errores antes de producción.
    """
    print("\n🛡️  INICIANDO PROTOCOLO DE PRE-VALIDACIÓN (Entorno: Mes 96)...")
    
    if not url or not key:
        print("❌ Error: Sin credenciales.")
        return

    try:
        client = create_custom_client(url, key)
        
        # 1. LIMPIEZA DEL ENTORNO DE PRUEBAS
        print("🧹 Limpiando Mes 96...")
        client.table("ejercicios").delete().eq("mes", 96).execute()

        # 2. GENERACIÓN Y CARGA DE DATOS V4.2
        print("⚙️  Generando datos V4.2 'Zero Redundancy'...")
        # Obtenemos la lista de los 2160 ejercicios
        datos_originales = seed_pure_splits_v4(execute_insert=False)
        
        # Ajustamos el mes a 96 para la prueba
        datos_test = []
        for d in datos_originales:
            nuevo_d = d.copy()
            nuevo_d["mes"] = 96
            datos_test.append(nuevo_d)

        print(f"📤 Inyectando {len(datos_test)} registros en Mes 96...")
        batch_size = 100
        for i in range(0, len(datos_test), batch_size):
            batch = datos_test[i:i + batch_size]
            client.table("ejercicios").insert(batch).execute()
        
        print("✅ Inyección de prueba completada.")

        # 3. AUDITORÍA DE CALIDAD SOBRE EL TEST
        print("\n🧐 Auditoría de Calidad sobre Mes 96:")
        errores = 0
        
        # Verificar un perfil al azar (Mujer, Pro, Definición)
        res = client.table("ejercicios").select("nombre").eq("mes", 96).eq("semana", 1).eq("genero", "Mujer").eq("nivel", "Pro").eq("objetivo", "Definición / Quema de Grasa").execute()
        
        ejercicios_semana = [r["nombre"] for r in res.data]
        conteo_total = len(ejercicios_semana)
        unicos = set(ejercicios_semana)

        print(f"   - Total ejercicios en la semana: {conteo_total} (Esperados: 30)")
        print(f"   - Ejercicios únicos: {len(unicos)} (Esperados: 30)")

        if conteo_total == 30 and len(unicos) == 30:
            print("   ✅ CALIDAD CONFIRMADA: Cero redundancia y volumen exacto.")
        else:
            print("   ❌ FALLO DE CALIDAD: Se detectaron duplicados o error de conteo.")
            errores += 1

        # 4. LIMPIEZA FINAL DEL TEST
        print("\n♻️  Vaciando entorno de pruebas...")
        client.table("ejercicios").delete().eq("mes", 96).execute()

        if errores == 0:
            print("\n✨ CONCLUSIÓN: El proceso es SEGURO para producción.")
            return True
        else:
            print("\n🚨 CONCLUSIÓN: El proceso tiene errores. ABORTANDO DESPLIEGUE.")
            return False

    except Exception as e:
        print(f"💥 Error crítico durante la validación: {e}")
        return False

if __name__ == "__main__":
    run_pre_deploy_validation()
