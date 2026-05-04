import os
from dotenv import load_dotenv
from supabase_config import create_custom_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def check_columns():
    client = create_custom_client(url, key)
    try:
        # Intentar obtener un registro para ver las columnas disponibles
        res = client.table("ejercicios").select("*").limit(1).execute()
        if res.data:
            print("Columnas actuales en 'ejercicios':")
            print(list(res.data[0].keys()))
        else:
            print("La tabla está vacía, no se pueden inferir columnas por datos.")
    except Exception as e:
        print(f"Error al inspeccionar columnas: {e}")

if __name__ == "__main__":
    check_columns()
