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
                        # --- DÍA 1: EMPUJE SUPERIOR (PECHO/HOMBRO FRONTAL/TRÍCEPS) ---
                        # Enfoque: Empuje Horizontal y Vertical + Aislamiento
                        base_push = [
                            {"nombre": "Press de Banca con Barra", "series": 4, "reps": 8, "descanso": 120}, # Empuje Base
                            {"nombre": "Press Militar con Barra", "series": 4, "reps": 10, "descanso": 90},  # Hombro Frontal
                            {"nombre": "Aperturas con Mancuernas (Flat)", "series": 3, "reps": 15, "descanso": 60}, # Estiramiento Pecho
                            {"nombre": "Elevaciones Laterales (Polea/Mancuerna)", "series": 4, "reps": 15, "descanso": 45}, # Hombro Lateral
                            {"nombre": "Press Francés con Barra Z", "series": 3, "reps": 12, "descanso": 60}, # Tríceps Cabeza Larga
                            {"nombre": "Fondos en Paralelas", "series": 3, "reps": 10, "descanso": 90}  # Empuje Compuesto Final
                        ]
                        
                        # --- DÍA 2: JALÓN SUPERIOR (ESPALDA/HOMBRO POSTERIOR/BÍCEPS) ---
                        # Enfoque: Tracción Vertical y Horizontal + Aislamiento
                        base_pull = [
                            {"nombre": "Dominadas Pronas", "series": 4, "reps": 10, "descanso": 120}, # Tracción Vertical
                            {"nombre": "Remo con Barra (Pendlay)", "series": 4, "reps": 8, "descanso": 120}, # Tracción Horizontal
                            {"nombre": "Jalón al Pecho Agarre Estrecho", "series": 3, "reps": 12, "descanso": 60}, # Latissimus Dorsi
                            {"nombre": "Pájaros con Mancuernas", "series": 4, "reps": 15, "descanso": 45}, # Hombro Posterior
                            {"nombre": "Curl Martillo con Mancuernas", "series": 3, "reps": 12, "descanso": 60}, # Braquial/Antebrazo
                            {"nombre": "Curl con Barra Z (Predicador)", "series": 3, "reps": 12, "descanso": 60} # Bíceps Pico
                        ]

                        # --- DÍA 3: EMPUJE INFERIOR (CUÁDRICEPS/PANTORRILLA) ---
                        # Enfoque: Dominancia de Rodilla
                        base_legs_push = [
                            {"nombre": "Sentadilla Trasera con Barra", "series": 4, "reps": 8, "descanso": 150}, # Compuesto Base
                            {"nombre": "Prensa de Piernas (Pies Bajos)", "series": 3, "reps": 15, "descanso": 120}, # Énfasis Cuádriceps
                            {"nombre": "Zancadas Búlgaras", "series": 3, "reps": 12, "descanso": 90}, # Unilateral
                            {"nombre": "Extensiones de Cuádriceps (Máquina)", "series": 3, "reps": 15, "descanso": 45}, # Aislamiento
                            {"nombre": "Elevación de Talones De Pie", "series": 4, "reps": 15, "descanso": 45}, # Gastrocnemio
                            {"nombre": "Sissy Squat (Cuerpo/Peso)", "series": 3, "reps": 15, "descanso": 60} # Estiramiento Terminal
                        ]

                        # --- DÍA 4: JALÓN INFERIOR (FEMORALES/GLÚTEOS) ---
                        # Enfoque: Dominancia de Cadera
                        base_legs_pull = [
                            {"nombre": "Peso Muerto Rumano (RDL)", "series": 4, "reps": 10, "descanso": 120}, # Cadena Posterior
                            {"nombre": "Hip Thrust con Barra", "series": 4, "reps": 10, "descanso": 120}, # Glúteo Mayor
                            {"nombre": "Curl de Pierna Acostado", "series": 3, "reps": 12, "descanso": 60}, # Femorales
                            {"nombre": "Kettlebell Swings (o Pull-through)", "series": 3, "reps": 20, "descanso": 60}, # Explosividad
                            {"nombre": "Abducciones en Máquina (Glúteo Medio)", "series": 3, "reps": 20, "descanso": 45}, # Estabilizadores
                            {"nombre": "Patada de Glúteo en Polea", "series": 3, "reps": 15, "descanso": 60} # Aislamiento Glúteo
                        ]

                        # --- DÍA 5: CORE & ESTABILIDAD DINÁMICA ---
                        # Enfoque: Anti-extensión, Anti-rotación e Hombros (Salud)
                        base_core = [
                            {"nombre": "Rueda Abdominal (Rollouts)", "series": 4, "reps": 12, "descanso": 60}, # Anti-extensión
                            {"nombre": "Press Pallof (Polea/Banda)", "series": 3, "reps": 15, "descanso": 45}, # Anti-rotación
                            {"nombre": "Elevación de Piernas (Colgado)", "series": 4, "reps": 15, "descanso": 60}, # Abdomen Inferior
                            {"nombre": "Plancha Lateral con Elevación", "series": 3, "reps": 45, "descanso": 45}, # Oblicuos
                            {"nombre": "Facepulls (Salud de Manguito)", "series": 4, "reps": 20, "descanso": 45}, # Retracción Escapular
                            {"nombre": "Deadbug Pro (Control Lumbar)", "series": 3, "reps": 12, "descanso": 45} # Estabilidad Profunda
                        ]

                        all_days = [
                            base_push,       # Día 1: Empuje Superior
                            base_legs_push, # Día 2: Empuje Inferior (Intercambiado)
                            base_pull,      # Día 3: Jalón Superior (Intercambiado)
                            base_legs_pull,  # Día 4: Jalón Inferior
                            base_core        # Día 5: Core
                        ]
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
