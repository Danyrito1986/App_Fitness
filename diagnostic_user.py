import db_manager as db
from models import User

def diagnostic_user():
    print("🧪 DIAGNÓSTICO DE DATOS DE USUARIO")
    try:
        client = db.get_supabase_client()
        user = db.get_user(client)
        
        if not user:
            print("❌ ERROR: No se pudo recuperar el usuario de la base de datos.")
            return

        print(f"✅ Usuario detectado: {user.nombre}")
        print(f"📊 Datos cargados:")
        print(f"  - Edad: {user.edad}")
        print(f"  - Peso: {user.peso_actual}")
        print(f"  - Altura: {user.altura}")
        print(f"  - Género: {user.genero}")
        print(f"  - Objetivo: {user.objetivo}")
        print(f"  - Cuello: {user.cuello}")
        print(f"  - Cintura: {user.cintura}")
        
        # Verificar si hay valores en 0 o None que puedan causar que se vea "vacío"
        missing = [k for k, v in user.__dict__.items() if v is None or v == 0]
        if missing:
            print(f"⚠️ AVISO: Campos con valor cero o nulos: {missing}")
        else:
            print("✨ Todos los campos críticos tienen datos.")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    diagnostic_user()
