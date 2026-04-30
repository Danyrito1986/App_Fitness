import os
import db_manager as db
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def check_duplicates():
    print("--- Verificando Estructura y Duplicados ---")
    try:
        res = supabase.table("usuarios").select("*").limit(1).execute()
        if res.data:
            print(f"Columnas detectadas: {list(res.data[0].keys())}")
        
        res_all = supabase.table("usuarios").select("*").execute()
        data = res_all.data
        # ... resto igual ...
        
        emails = {}
        for row in data:
            email = row.get("email") or row.get("correo")
            if not email:
                print(f"ALERTA: Registro sin email/correo: ID {row['id']} - Nombre {row.get('nombre')}")
                continue
            
            if email in emails:
                emails[email].append(row["id"])
            else:
                emails[email] = [row["id"]]
        
        duplicates = {e: ids for e, ids in emails.items() if len(ids) > 1}
        
        if duplicates:
            print(f"\n¡SE ENCONTRARON DUPLICADOS! ({len(duplicates)} correos)")
            for email, ids in duplicates.items():
                print(f" - {email}: IDs {ids}")
        else:
            print("\nNo se encontraron correos duplicados.")
            
    except Exception as e:
        print(f"Error al consultar: {e}")

if __name__ == "__main__":
    check_duplicates()
