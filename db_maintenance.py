import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: No se encontraron las variables de entorno SUPABASE_URL o SUPABASE_KEY.")
    sys.exit(1)

supabase: Client = create_client(url, key)

def mostrar_menu():
    print("\n" + "="*40)
    print("   CENTRO DE MANTENIMIENTO APP FITNESS")
    print("="*40)
    print("1. Cargar Ejercicios Base (Gimnasio Convencional)")
    print("2. Verificar y Limpiar Usuarios Duplicados")
    print("3. Limpiar Todas las Rutinas y Ejercicios")
    print("4. Auditar Tabla 'usuarios' (Estructura)")
    print("5. Salir")
    print("="*40)

def seed_ejercicios():
    print("\nIniciando carga de ejercicios...")
    # Importar lógica desde master_seeding o implementarla aquí directamente para independencia
    try:
        from master_seeding import seed_masivo
        seed_masivo()
    except ImportError:
        print("Error: No se encontró master_seeding.py para importar la lógica.")

def auditar_usuarios():
    print("\nAuditoría de Tabla 'usuarios':")
    try:
        res = supabase.table("usuarios").select("*").limit(1).execute()
        if res.data:
            print(f"Columnas detectadas: {list(res.data[0].keys())}")
            print(f"Total de usuarios registrados: {len(supabase.table('usuarios').select('id').execute().data)}")
        else:
            print("La tabla está vacía.")
    except Exception as e:
        print(f"Error: {e}")

def limpiar_tablas():
    confirmar = input("\n¿ESTÁS SEGURO? Esto borrará TODOS los ejercicios y rutinas (y/n): ")
    if confirmar.lower() == 'y':
        try:
            supabase.table("ejercicios").delete().neq("id", 0).execute()
            print("¡Tablas limpiadas con éxito!")
        except Exception as e:
            print(f"Error al limpiar: {e}")

def verificar_duplicados():
    print("\nVerificando correos duplicados...")
    try:
        res = supabase.table("usuarios").select("id, email, nombre").execute()
        emails = {}
        for row in res.data:
            email = row.get("email")
            if email:
                if email in emails:
                    emails[email].append(row["id"])
                else:
                    emails[email] = [row["id"]]
        
        duplicates = {k: v for k, v in emails.items() if len(v) > 1}
        if duplicates:
            print(f"Se encontraron {len(duplicates)} correos con múltiples registros:")
            for email, ids in duplicates.items():
                print(f" - {email}: IDs {ids}")
        else:
            print("No se encontraron duplicados.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            seed_ejercicios()
        elif opcion == "2":
            verificar_duplicados()
        elif opcion == "3":
            limpiar_tablas()
        elif opcion == "4":
            auditar_usuarios()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
