import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def fix_db_structure():
    print("🛠️ INICIANDO CORRECCIÓN DE BASE DE DATOS...")
    try:
        supabase = create_client(url, key)
        
        # 1. Verificar si existe la tabla progreso_series
        print("🔍 Verificando tabla 'progreso_series'...")
        try:
            res = supabase.table("progreso_series").select("*").limit(1).execute()
            print("✅ Tabla 'progreso_series' existe.")
        except Exception as e:
            print(f"❌ Error accediendo a 'progreso_series': {e}")
            print("💡 Sugerencia: Crea la tabla en Supabase SQL Editor:")
            print("""
            CREATE TABLE progreso_series (
                id BIGSERIAL PRIMARY KEY,
                usuario_id BIGINT REFERENCES usuarios(id),
                fecha DATE NOT NULL,
                datos JSONB DEFAULT '{}'::jsonb,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            ALTER TABLE progreso_series ENABLE ROW LEVEL SECURITY;
            CREATE POLICY "Acceso total" ON progreso_series FOR ALL USING (true);
            """)

        # 2. Verificar tabla usuarios
        print("\n🔍 Verificando tabla 'usuarios'...")
        try:
            res = supabase.table("usuarios").select("*").limit(1).execute()
            if res.data:
                u = res.data[0]
                print(f"✅ Tabla 'usuarios' accesible. Columnas detectadas: {list(u.keys())}")
                
                # Verificar columnas críticas
                cols = list(u.keys())
                missing = [c for c in ["genero", "nivel", "mes_actual", "entrenos_mes"] if c not in cols]
                if missing:
                    print(f"⚠️ Faltan columnas en 'usuarios': {missing}")
                else:
                    print("✨ Estructura de 'usuarios' parece correcta.")
            else:
                print("⚠️ La tabla 'usuarios' está vacía.")
        except Exception as e:
            print(f"❌ Error en 'usuarios': {e}")

        # 3. Test de escritura simple (Upsert)
        print("\n🧪 Probando escritura (Upsert)...")
        test_data = {"usuario_id": 1, "fecha": "2026-05-15", "datos": {"test": True}}
        try:
            # Intento de upsert usando select + insert/update
            res = supabase.table("progreso_series").select("id").eq("usuario_id", 1).eq("fecha", "2026-05-15").execute()
            if res.data:
                print("📝 Actualizando registro de prueba...")
                supabase.table("progreso_series").update({"datos": {"test": True, "updated": True}}).eq("id", res.data[0]["id"]).execute()
            else:
                print("📝 Insertando registro de prueba...")
                supabase.table("progreso_series").insert(test_data).execute()
            print("✅ Prueba de escritura exitosa.")
        except Exception as e:
            print(f"❌ Fallo en prueba de escritura: {e}")

    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")

if __name__ == "__main__":
    fix_db_structure()
