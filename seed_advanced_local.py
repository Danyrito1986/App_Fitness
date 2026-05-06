import os
from dotenv import load_dotenv
from supabase_config import create_custom_client

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def seed_advanced_exercises(execute_insert=False):
    """
    Genera y (opcionalmente) inserta rutinas para el nivel 'Avanzado'.
    Mantiene la estructura de Patrones Puros V4.
    """
    print("\n🚀 Preparando Rutinas Nivel AVANZADO (V4)...")
    
    if execute_insert:
        print("⚠️  AVISO: execute_insert está en True, se realizarán cambios en Supabase.")
    else:
        print("💡 MODO SIMULACIÓN: No se realizarán cambios.")

    ejercicios = []
    # Solo nivel Avanzado para este script específico
    niveles = ["Avanzado"]
    generos = ["Hombre", "Mujer"]
    objetivos = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Resistencia"]
    semanas = [1, 2, 3, 4]
    meses = [1, 2, 3] # Poblamos 3 meses de una vez para Avanzado

    for g in generos:
        for n in niveles:
            for obj in objetivos:
                for mes in meses:
                    for sem in semanas:
                        # --- DÍA 1: EMPUJE SUPERIOR ---
                        base_push = [
                            {"nombre": "Press de Banca Inclinado (Barra)", "series": 4, "reps": 6, "descanso": 150},
                            {"nombre": "Press Militar con Mancuernas", "series": 4, "reps": 8, "descanso": 120},
                            {"nombre": "Cruces en Polea (Pecho)", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Elevaciones Laterales (Polea)", "series": 4, "reps": 15, "descanso": 45},
                            {"nombre": "Extensiones de Tríceps (Cuerda)", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Dips (Fondos) con Lastre", "series": 3, "reps": 8, "descanso": 120}
                        ]
                        
                        # --- DÍA 2: EMPUJE INFERIOR ---
                        base_legs_push = [
                            {"nombre": "Sentadilla Frontal con Barra", "series": 4, "reps": 6, "descanso": 180},
                            {"nombre": "Hack Squat (Máquina)", "series": 3, "reps": 10, "descanso": 120},
                            {"nombre": "Split Squat (Mancuernas)", "series": 3, "reps": 12, "descanso": 90},
                            {"nombre": "Sissy Squat (con Disco)", "series": 3, "reps": 15, "descanso": 60},
                            {"nombre": "Elevación de Talones (Prensa)", "series": 4, "reps": 20, "descanso": 45},
                            {"nombre": "Tibia Anterior (Opcional/Salud)", "series": 2, "reps": 15, "descanso": 30}
                        ]

                        # --- DÍA 3: JALÓN SUPERIOR ---
                        base_pull = [
                            {"nombre": "Dominadas Lastradas", "series": 4, "reps": 6, "descanso": 150},
                            {"nombre": "Remo con Barra T", "series": 4, "reps": 8, "descanso": 120},
                            {"nombre": "Pullover en Polea Alta", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Facepulls (Salud)", "series": 3, "reps": 20, "descanso": 45},
                            {"nombre": "Curl de Bíceps con Barra Z", "series": 3, "reps": 10, "descanso": 60},
                            {"nombre": "Curl Martillo (Banco Inclinado)", "series": 3, "reps": 12, "descanso": 60}
                        ]

                        # --- DÍA 4: JALÓN INFERIOR ---
                        base_legs_pull = [
                            {"nombre": "Peso Muerto Convencional", "series": 3, "reps": 5, "descanso": 180},
                            {"nombre": "Hamstring Curls (Sentado)", "series": 4, "reps": 12, "descanso": 60},
                            {"nombre": "Glute Ham Raise (GHR)", "series": 3, "reps": 10, "descanso": 90},
                            {"nombre": "Hip Thrust (Pausa 2s)", "series": 4, "reps": 10, "descanso": 120},
                            {"nombre": "Buenos Días (Mancuerna/Barra)", "series": 3, "reps": 12, "descanso": 90},
                            {"nombre": "Abducción de Cadera (Polea)", "series": 3, "reps": 15, "descanso": 45}
                        ]

                        # --- DÍA 5: CORE & COMPLEMENTOS ---
                        base_core = [
                            {"nombre": "Dragon Flags (o Progresión)", "series": 4, "reps": 8, "descanso": 90},
                            {"nombre": "L-Sit Holds", "series": 4, "reps": 30, "descanso": 60},
                            {"nombre": "Woodchoppers (Polea)", "series": 3, "reps": 15, "descanso": 45},
                            {"nombre": "Plancha con Peso (Lastre)", "series": 3, "reps": 60, "descanso": 60},
                            {"nombre": "Crunches en Polea", "series": 4, "reps": 15, "descanso": 60},
                            {"nombre": "Hollow Hold (Rocas)", "series": 3, "reps": 45, "descanso": 45}
                        ]

                        all_days = [base_push, base_legs_push, base_pull, base_legs_pull, base_core]
                        for d_idx, day_exercises in enumerate(all_days):
                            for ex in day_exercises:
                                final_ex = ex.copy()
                                # Ajustes por semana
                                if sem == 2: final_ex["series"] += 1
                                if sem == 3: 
                                    final_ex["reps"] = max(4, final_ex["reps"] - 2)
                                    final_ex["descanso"] += 30
                                if sem == 4: # Descarga
                                    final_ex["series"] = 2
                                    final_ex["reps"] = 12
                                
                                final_ex.update({
                                    "genero": g, "nivel": n, "objetivo": obj,
                                    "mes": mes, "semana": sem, "dia": d_idx + 1
                                })
                                ejercicios.append(final_ex)

    print(f"✅ Simulación completada: {len(ejercicios)} ejercicios generados para nivel AVANZADO.")
    
    if execute_insert:
        try:
            client = create_custom_client(url, key)
            batch_size = 100
            for i in range(0, len(ejercicios), batch_size):
                batch = ejercicios[i:i + batch_size]
                client.table("ejercicios").insert(batch).execute()
                print(f"📦 Insertados {i + len(batch)} / {len(ejercicios)}")
            print("✨ ¡Nivel Avanzado inyectado con éxito!")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⏭️  No se realizaron cambios en Supabase (Modo Simulación).")

    return ejercicios

if __name__ == "__main__":
    # Cambiado a True para ejecución real tras validación
    seed_advanced_exercises(execute_insert=True)
