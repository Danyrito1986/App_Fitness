import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def seed_masivo():
    print("Iniciando carga masiva de biblioteca de ejercicios Pro...")
    
    # 1. Limpiar ejercicios anteriores (opcional, pero ayuda a evitar duplicados en pruebas)
    # supabase.table("ejercicios").delete().neq("id", 0).execute()

    ejercicios = []
    
    niveles = ["Novato", "Intermedio", "Pro"]
    generos = ["Hombre", "Mujer"]
    # Nota: Los objetivos deben coincidir exactamente con los del Dropdown en profile_view.py
    objetivos = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Resistencia"]
    
    for g in generos:
        for n in niveles:
            for obj in objetivos:
                # Lógica de intensidad
                reps_base = 10 if obj == "Aumento de masa muscular" else 15
                if obj == "Resistencia": reps_base = 12
                
                series_base = 3 if n == "Novato" else 4
                if n == "Pro": series_base = 5

                # Mes 1 - Día 1: Empuje (Pecho/Hombro/Tricep)
                ejercicios.append({"nombre": "Press de Banca con Mancuernas", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Aperturas en Polea", "series": series_base, "reps": reps_base + 2, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Press Militar Mancuernas", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Extensión Tricep Polea", "series": series_base, "reps": reps_base + 3, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 45})
                
                # Mes 1 - Día 2: Tracción (Espalda/Bicep)
                ejercicios.append({"nombre": "Jalón al Pecho", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Remo con Mancuerna", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Curl de Bicep Barra Z", "series": series_base, "reps": reps_base + 2, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Martillos", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})

                # Mes 1 - Día 3: Pierna (Énfasis Cuádriceps)
                sentadilla = "Sentadilla Goblet" if n == "Novato" else "Sentadilla con Barra"
                ejercicios.append({"nombre": sentadilla, "series": series_base + 1, "reps": reps_base - 2, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 90})
                ejercicios.append({"nombre": "Extensiones de Cuádriceps", "series": series_base, "reps": reps_base + 5, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Prensa Inclinada", "series": series_base, "reps": reps_base, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Zancadas", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 60})

                # Mes 1 - Día 4: Hombro Lateral y Abdomen
                ejercicios.append({"nombre": "Elevaciones Laterales", "series": series_base, "reps": reps_base + 5, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Pájaros (Hombro Posterior)", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Crunch en Polea", "series": 4, "reps": 20, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Plancha Isométrica", "series": 3, "reps": 60, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})

                # Mes 1 - Día 5: Full Body / Cardio
                ejercicios.append({"nombre": "Burpees", "series": 3, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                ejercicios.append({"nombre": "Kettlebell Swings", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 45})
                ejercicios.append({"nombre": "Escaladores", "series": 3, "reps": 30, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 30})

    print(f"Total de ejercicios preparados: {len(ejercicios)}")
    
    # Inserción por lotes
    batch_size = 40
    for i in range(0, len(ejercicios), batch_size):
        batch = ejercicios[i:i+batch_size]
        try:
            supabase.table("ejercicios").insert(batch).execute()
            print(f"Lote {i//batch_size + 1} inyectado con éxito.")
        except Exception as e:
            print(f"Error en lote {i//batch_size + 1}: {e}")

    print("Carga masiva finalizada con éxito.")

if __name__ == "__main__":
    seed_masivo()
