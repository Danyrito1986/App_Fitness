import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def seed_masivo():
    print("Iniciando carga masiva de biblioteca de ejercicios GIMNASIO CONVENCIONAL...")
    
    # 1. Limpiar ejercicios anteriores para evitar basura
    try:
        supabase.table("ejercicios").delete().neq("id", 0).execute()
        print("Base de datos de ejercicios limpia.")
    except Exception as e:
        print(f"Error limpiando: {e}")

    ejercicios = []
    niveles = ["Novato", "Intermedio", "Pro"]
    generos = ["Hombre", "Mujer"]
    objetivos = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Resistencia"]
    
    for g in generos:
        for n in niveles:
            for obj in objetivos:
                # --- CONFIGURACIÓN DE VOLUMEN E INTENSIDAD ---
                reps_base = 10 if obj == "Aumento de masa muscular" else 15
                if obj == "Resistencia": reps_base = 12
                
                series_base = 3 if n == "Novato" else 4
                if n == "Pro": series_base = 5

                # --- DÍA 1: PECHO, HOMBRO FRONTAL Y TRÍCEPS (EMPUJE) ---
                if n == "Novato":
                    ejercicios.append({"nombre": "Press de Pecho en Máquina Sentado para Estabilidad", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Aperturas en Contratransfer (Pec-Deck) para Pecho", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Press Militar en Máquina para Hombro Frontal", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Extensión de Tríceps en Polea con Cuerda", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 45})
                elif n == "Intermedio":
                    ejercicios.append({"nombre": "Press de Banca Plano con Barra para Pecho", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Press Inclinado con Mancuernas para Pecho Superior", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Press Militar con Mancuernas para Hombro", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 75})
                    ejercicios.append({"nombre": "Copa a una mano con Mancuerna para Tríceps", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})
                else: # PRO
                    ejercicios.append({"nombre": "Press Inclinado con Barra (Pausa en Pecho) para Hipertrofia", "series": 5, "reps": 8, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Fondos en Paralelas con Lastre para Pecho Inferior", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Cruce de Poleas Altas para Detalle de Pecho", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Press Arnold con Mancuernas para Hombro Completo", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 75})
                    ejercicios.append({"nombre": "Press Francés con Barra Z para Tríceps", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 1, "objetivo": obj, "descanso": 60})

                # --- DÍA 2: ESPALDA, HOMBRO POSTERIOR Y BÍCEPS (TRACCIÓN) ---
                if n == "Novato":
                    ejercicios.append({"nombre": "Jalón al Pecho en Polea para Dorsales", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Remo en Máquina Sentado para Espalda Media", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Face-Pulls en Polea para Hombro Posterior", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Curl de Bíceps en Máquina para Aislamiento", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                elif n == "Intermedio":
                    ejercicios.append({"nombre": "Remo con Barra para Grosor de Espalda", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Dominadas Asistidas o Libres para Espalda", "series": 4, "reps": 8, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Remo con Mancuerna a una mano para Dorsal", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Curl de Bíceps con Barra Z para Fuerza", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 75})
                else: # PRO
                    ejercicios.append({"nombre": "Remo con Barra T Pesado para Espalda", "series": 5, "reps": 8, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Jalón con Agarre Estrecho para Dorsal Inferior", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Pull-Over en Polea Alta para Serratos y Dorsal", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Pájaros con Mancuerna para Hombro Posterior", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Curl Martillo Pesado para Braquial y Bíceps", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 2, "objetivo": obj, "descanso": 75})

                # --- DÍA 3: PIERNA (CUÁDRICEPS Y PANTORRILLA) ---
                if n == "Novato":
                    ejercicios.append({"nombre": "Prensa Inclinada para Cuádriceps", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Extensiones de Cuádriceps en Máquina", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Curl de Pierna Sentado para Isquios", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Elevación de Talones en Máquina para Pantorrilla", "series": 4, "reps": 20, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 45})
                elif n == "Intermedio":
                    ejercicios.append({"nombre": "Sentadilla con Barra para Fuerza de Piernas", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Zancadas con Mancuernas para Glúteos y Pierna", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 75})
                    ejercicios.append({"nombre": "Peso Muerto Rumano con Mancuernas para Isquios", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Costurero (Pantorrilla Sentado)", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 45})
                else: # PRO
                    ejercicios.append({"nombre": "Sentadilla Búlgara con Mancuernas para Pierna Pro", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Hack Squat (Sentadilla Hack) para Cuádriceps", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Peso Muerto con Barra para Cadena Posterior", "series": 5, "reps": 8, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 180})
                    ejercicios.append({"nombre": "Curl de Pierna Tumbado con Pausa", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 3, "objetivo": obj, "descanso": 60})

                # --- DÍA 4: HOMBRO LATERAL, TRAPECIO Y ABDOMEN ---
                if n == "Novato":
                    ejercicios.append({"nombre": "Elevaciones Laterales en Máquina o Polea", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Encogimientos en Máquina para Trapecio", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Crunch Abdominal en Máquina", "series": 4, "reps": 20, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Plancha Isométrica Frontal para Core", "series": 3, "reps": 60, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})
                elif n == "Intermedio":
                    ejercicios.append({"nombre": "Elevaciones Laterales con Mancuernas Pesadas", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Remo al Mentón con Barra Z para Hombro y Trapecio", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Elevación de Piernas Colgado para Abdomen", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Rueda Abdominal para Estabilidad de Core", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})
                else: # PRO
                    ejercicios.append({"nombre": "Elevaciones Laterales (Drop Sets) con Mancuerna", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 30})
                    ejercicios.append({"nombre": "Encogimientos con Barra Pesada para Trapecio", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 75})
                    ejercicios.append({"nombre": "V-Ups (Abdominales en V) para Core", "series": 4, "reps": 20, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Crunch en Polea con Cuerda Pesado", "series": 4, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 4, "objetivo": obj, "descanso": 60})

                # --- DÍA 5: ISQUIOSURALES, GLÚTEO Y BRAZO COMPLETO ---
                if n == "Novato":
                    ejercicios.append({"nombre": "Hip Thrust en Máquina para Glúteos", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 90})
                    ejercicios.append({"nombre": "Abductores en Máquina para Glúteo Medio", "series": 3, "reps": 20, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Curl de Bíceps en Polea Baja", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Extensión de Tríceps por encima de la cabeza", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                elif n == "Intermedio":
                    ejercicios.append({"nombre": "Hip Thrust con Barra Libre para Glúteos", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Patada de Glúteo en Polea", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 45})
                    ejercicios.append({"nombre": "Curl Concentrado con Mancuerna para Bíceps", "series": 3, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Dippings (Fondos en Banco) para Tríceps", "series": 3, "reps": 15, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                else: # PRO
                    ejercicios.append({"nombre": "Peso Muerto Rumano Pesado para Isquios", "series": 5, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Hip Thrust con Lastre y Pausa de 2s", "series": 4, "reps": 8, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 120})
                    ejercicios.append({"nombre": "Curl de Bíceps Inclinado con Mancuernas", "series": 4, "reps": 12, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 60})
                    ejercicios.append({"nombre": "Press Cerrado con Barra para Tríceps", "series": 4, "reps": 10, "genero": g, "nivel": n, "mes": 1, "dia": 5, "objetivo": obj, "descanso": 90})

    print(f"Total de ejercicios preparados: {len(ejercicios)}")
    
    # Inserción por lotes
    batch_size = 50
    for i in range(0, len(ejercicios), batch_size):
        batch = ejercicios[i:i+batch_size]
        try:
            supabase.table("ejercicios").insert(batch).execute()
            print(f"Lote {i//batch_size + 1} inyectado con éxito.")
        except Exception as e:
            print(f"Error en lote {i//batch_size + 1}: {e}")

    print("Carga masiva de GIMNASIO finalizada con éxito.")

if __name__ == "__main__":
    seed_masivo()
