import os
from dotenv import load_dotenv
from supabase_config import create_custom_client

# Cargar configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

def seed_pure_splits_v4(execute_insert=False):
    """
    Biblioteca de ejercicios organizada por Patrones Puros:
    Día 1: Empuje Superior (Chest, Shoulder, Triceps)
    Día 2: Jalón Superior (Back, Biceps)
    Día 3: Empuje Inferior (Quads, Calves)
    Día 4: Jalón Inferior (Hamstrings, Glutes)
    Día 5: Core (Abs, Lower Back)
    """
    print("\n🚀 Preparando Biblioteca de Ejercicios PUROS V4...")
    
    if not url or not key:
        print("❌ Error: No se encontraron credenciales en el .env")
        return

    ejercicios = []
    niveles = ["Novato", "Intermedio", "Pro"]
    generos = ["Hombre", "Mujer"]
    objetivos = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Resistencia"]
    semanas = [1, 2, 3, 4]
    meses = [1] 

    for g in generos:
        for n in niveles:
            for obj in objetivos:
                for mes in meses:
                    for sem in semanas:
                        # --- DÍA 1: EMPUJE SUPERIOR (PROFESIONAL) ---
                        base_push = [
                            {"nombre": "Press de Banca con Barra", "series": 4, "reps": 8, "descanso": 120},
                            {"nombre": "Press Inclinado con Mancuernas", "series": 3, "reps": 12, "descanso": 90},
                            {"nombre": "Press Militar con Barra", "series": 4, "reps": 10, "descanso": 90},
                            {"nombre": "Elevaciones Laterales (Hombro)", "series": 4, "reps": 15, "descanso": 45},
                            {"nombre": "Fondos de Pecho/Tríceps", "series": 3, "reps": 12, "descanso": 90},
                            {"nombre": "Extensión de Tríceps en Polea", "series": 3, "reps": 15, "descanso": 45}
                        ]
                        
                        # --- DÍA 2: JALÓN SUPERIOR (PROFESIONAL) ---
                        base_pull = [
                            {"nombre": "Dominadas (o Jalón al Pecho)", "series": 4, "reps": 10, "descanso": 120},
                            {"nombre": "Remo con Barra (Pendlay)", "series": 4, "reps": 8, "descanso": 120},
                            {"nombre": "Remo con Mancuerna a una mano", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Pájaros (Hombro Posterior)", "series": 4, "reps": 15, "descanso": 45},
                            {"nombre": "Curl de Bíceps con Barra", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Curl Martillo con Mancuernas", "series": 3, "reps": 12, "descanso": 60}
                        ]

                        # --- DÍA 3: EMPUJE INFERIOR (PROFESIONAL) ---
                        base_legs_push = [
                            {"nombre": "Sentadilla Libre con Barra", "series": 4, "reps": 8, "descanso": 150},
                            {"nombre": "Prensa de Piernas 45°", "series": 3, "reps": 15, "descanso": 120},
                            {"nombre": "Zancadas con Mancuernas", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Extensiones de Cuádriceps", "series": 3, "reps": 15, "descanso": 45},
                            {"nombre": "Elevación de Talones De Pie", "series": 4, "reps": 15, "descanso": 45},
                            {"nombre": "Elevación de Talones Sentado", "series": 3, "reps": 20, "descanso": 45}
                        ]

                        # --- DÍA 4: JALÓN INFERIOR (PROFESIONAL) ---
                        base_legs_pull = [
                            {"nombre": "Peso Muerto Rumano (RDL)", "series": 4, "reps": 10, "descanso": 120},
                            {"nombre": "Hip Thrust con Barra", "series": 4, "reps": 10, "descanso": 120},
                            {"nombre": "Curl de Pierna Acostado", "series": 3, "reps": 12, "descanso": 60},
                            {"nombre": "Curl de Pierna Sentado", "series": 3, "reps": 15, "descanso": 60},
                            {"nombre": "Abducción de Cadera (Máquina)", "series": 3, "reps": 20, "descanso": 45},
                            {"nombre": "Buenos Días con Barra", "series": 3, "reps": 15, "descanso": 90}
                        ]

                        # --- DÍA 5: CORE & COMPLEMENTOS (PROFESIONAL) ---
                        base_core = [
                            {"nombre": "Rueda Abdominal", "series": 4, "reps": 12, "descanso": 60},
                            {"nombre": "Elevación de Piernas Colgado", "series": 4, "reps": 15, "descanso": 60},
                            {"nombre": "Plancha Abdominal Pro", "series": 4, "reps": 60, "descanso": 45},
                            {"nombre": "Crunch con Cable (Polea)", "series": 3, "reps": 20, "descanso": 45},
                            {"nombre": "Hiperextensiones Lumbares", "series": 3, "reps": 15, "descanso": 60},
                            {"nombre": "Facepulls (Salud de Hombro)", "series": 3, "reps": 20, "descanso": 45}
                        ]

                        all_days = [base_push, base_pull, base_legs_push, base_legs_pull, base_core]
                        for d_idx, day_exercises in enumerate(all_days):
                            for ex in day_exercises:
                                final_ex = ex.copy()
                                # Lógica de progresión
                                if sem == 2: final_ex["series"] += 1
                                if sem == 3: 
                                    final_ex["reps"] = max(6, final_ex["reps"] - 2)
                                    final_ex["descanso"] += 30
                                if sem == 4:
                                    final_ex["series"] = 2
                                    final_ex["reps"] = 12
                                
                                final_ex.update({
                                    "genero": g, "nivel": n, "objetivo": obj,
                                    "mes": mes, "semana": sem, "dia": d_idx + 1
                                })
                                ejercicios.append(final_ex)

    print(f"📊 Total de ejercicios generados: {len(ejercicios)}")

    if execute_insert:
        print(f"⚠️  INICIANDO INSERCIÓN REAL EN SUPABASE...")
        try:
            client = create_custom_client(url, key)
            
            # Limpiar ejercicios previos del Mes 1 para evitar duplicados (Opcional pero recomendado)
            # print("🧹 Limpiando ejercicios antiguos del Mes 1...")
            # client.table("ejercicios").delete().eq("mes", 1).execute()

            # Insertar por lotes de 100 para estabilidad
            batch_size = 100
            for i in range(0, len(ejercicios), batch_size):
                batch = ejercicios[i:i + batch_size]
                client.table("ejercicios").insert(batch).execute()
                print(f"✅ Insertados {i + len(batch)} / {len(ejercicios)}")
            
            print("\n✨ ¡Biblioteca V4 inyectada con éxito!")
        except Exception as e:
            print(f"❌ Error durante la inyección: {e}")
    else:
        print("\n💡 MODO PREVISUALIZACIÓN: No se realizaron cambios en la base de datos.")
        print("Para ejecutar la inyección, cambia a: seed_pure_splits_v4(execute_insert=True)")

    return ejercicios

if __name__ == "__main__":
    # Cambiar a True para ejecutar la subida real
    seed_pure_splits_v4(execute_insert=True)
