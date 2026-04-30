import os
from supabase import create_client
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def cargar_ejercicios():
    print("DEBUG: Detectando columnas de la tabla 'ejercicios'...")
    try:
        sample = supabase.table("ejercicios").select("*").limit(1).execute()
        if sample.data:
            print(f"Columnas detectadas: {list(sample.data[0].keys())}")
        else:
            print("La tabla está vacía, no se pueden detectar columnas por muestra.")
    except Exception as e:
        print(f"Error al inspeccionar tabla: {e}")


if __name__ == "__main__":
    cargar_ejercicios()
