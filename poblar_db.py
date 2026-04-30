import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def poblar_todo():
    print("1. Creando Rutinas base...")
    rutinas = [
        {"id": 1, "nombre": "Día 1: Pecho y Tricep"},
        {"id": 2, "nombre": "Día 2: Espalda y Bicep"},
        {"id": 3, "nombre": "Día 3: Pierna"},
        {"id": 4, "nombre": "Día 4: Hombro y Abs"},
        {"id": 5, "nombre": "Día 5: Full Body"}
    ]
    try:
        # Usamos upsert para no duplicar si ya existen
        supabase.table("rutinas").upsert(rutinas).execute()
        print("¡Rutinas listas!")

        print("2. Subiendo Ejercicios vinculados...")
        ejercicios = [
            {"nombre": "Press de Banca", "series": 4, "reps": 12, "rutina_id": 1, "descanso": 60},
            {"nombre": "Aperturas", "series": 3, "reps": 15, "rutina_id": 1, "descanso": 60},
            {"nombre": "Jalón al Pecho", "series": 4, "reps": 12, "rutina_id": 2, "descanso": 60},
            {"nombre": "Curl de Bicep", "series": 3, "reps": 15, "rutina_id": 2, "descanso": 45},
            {"nombre": "Sentadilla", "series": 4, "reps": 10, "rutina_id": 3, "descanso": 90},
            {"nombre": "Prensa", "series": 3, "reps": 12, "rutina_id": 3, "descanso": 60},
            {"nombre": "Press Militar", "series": 4, "reps": 12, "rutina_id": 4, "descanso": 60},
            {"nombre": "Crunch", "series": 4, "reps": 20, "rutina_id": 4, "descanso": 30},
            {"nombre": "Burpees", "series": 3, "reps": 10, "rutina_id": 5, "descanso": 60},
            {"nombre": "Plancha", "series": 3, "reps": 45, "rutina_id": 5, "descanso": 45}
        ]
        supabase.table("ejercicios").insert(ejercicios).execute()
        print("¡Ejercicios cargados con éxito!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    poblar_todo()
