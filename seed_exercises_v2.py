import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def cargar_ejercicios_v2():
    # Usaremos rutina_id para marcar los días (1 al 5)
    ejercicios = [
        # DIA 1 (rutina_id: 1)
        {"nombre": "Press de Banca con Barra", "series": 4, "reps": 12, "rutina_id": 1, "descanso": 60},
        {"nombre": "Aperturas con Mancuernas", "series": 3, "reps": 15, "rutina_id": 1, "descanso": 60},
        {"nombre": "Flexiones de Pecho", "series": 3, "reps": 10, "rutina_id": 1, "descanso": 45},
        
        # DIA 2 (rutina_id: 2)
        {"nombre": "Jalón al Pecho", "series": 4, "reps": 12, "rutina_id": 2, "descanso": 60},
        {"nombre": "Remo con Mancuerna", "series": 3, "reps": 12, "rutina_id": 2, "descanso": 60},
        {"nombre": "Curl de Bicep", "series": 3, "reps": 15, "rutina_id": 2, "descanso": 45},

        # DIA 3 (rutina_id: 3)
        {"nombre": "Sentadilla con Barra", "series": 4, "reps": 10, "rutina_id": 3, "descanso": 90},
        {"nombre": "Prensa de Piernas", "series": 3, "reps": 12, "rutina_id": 3, "descanso": 60},
        {"nombre": "Extensiones", "series": 3, "reps": 15, "rutina_id": 3, "descanso": 45},

        # DIA 4 (rutina_id: 4)
        {"nombre": "Press Militar", "series": 4, "reps": 12, "rutina_id": 4, "descanso": 60},
        {"nombre": "Elevaciones Laterales", "series": 3, "reps": 15, "rutina_id": 4, "descanso": 45},
        {"nombre": "Crunch Abdominal", "series": 4, "reps": 20, "rutina_id": 4, "descanso": 30},

        # DIA 5 (rutina_id: 5)
        {"nombre": "Burpees", "series": 3, "reps": 10, "rutina_id": 5, "descanso": 60},
        {"nombre": "Zancadas", "series": 3, "reps": 12, "rutina_id": 5, "descanso": 60},
        {"nombre": "Plancha", "series": 3, "reps": 45, "rutina_id": 5, "descanso": 45},
    ]

    print("Subiendo rutina base del Mes 1...")
    try:
        supabase.table("ejercicios").insert(ejercicios).execute()
        print("¡Rutina cargada con éxito!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cargar_ejercicios_v2()
