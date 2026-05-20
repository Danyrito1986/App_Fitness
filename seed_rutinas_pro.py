import os
import time
from supabase import create_client, Client
from dotenv import load_dotenv

# Carga de credenciales
load_dotenv('D:/Proyects/App_Fitness/.env')
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- POOLS DE EJERCICIOS POR COMPLEJIDAD ---
# Estructura: (Nombre, Es_Maquinas_Novato)
EX_POOLS = {
    "SUPERIOR_PUSH": [
        ("Press de Banca con Barra", False), ("Press Militar con Barra", False), 
        ("Aperturas con Mancuernas", False), ("Elevaciones Laterales", False), 
        ("Press Frances", False), ("Fondos en Paralelas", False),
        ("Press Inclinado con Mancuernas", False), ("Cruce de Poleas", True),
        ("Press de Pecho en Maquina", True), ("Press de Hombro en Maquina", True)
    ],
    "SUPERIOR_PULL": [
        ("Dominadas Pronas", False), ("Remo con Barra", False), 
        ("Jalon al Pecho", True), ("Pajaros con Mancuernas", False), 
        ("Curl Martillo", False), ("Curl con Barra Z", False),
        ("Remo en Polea Baja", True), ("Facepulls", True),
        ("Remo en Maquina", True), ("Biceps en Maquina", True)
    ],
    "INFERIOR_CUAD": [
        ("Sentadilla Trasera", False), ("Prensa de Piernas", True), 
        ("Zancadas Bulgaras", False), ("Extensiones de Cuadriceps", True), 
        ("Sissy Squat", False), ("Hack Squat", True), ("Sentadilla Goblet", False)
    ],
    "INFERIOR_POSTERIOR": [
        ("Peso Muerto Rumano", False), ("Hip Thrust con Barra", False), 
        ("Curl de Pierna Acostado", True), ("Kettlebell Swings", False), 
        ("Abducciones en Maquina", True), ("Patada de Gluteo", True), ("Peso Muerto Sumo", False)
    ],
    "CORE_MIX": [
        ("Rueda Abdominal", False), ("Elevacion de Piernas", False), 
        ("Press Pallof", True), ("Plancha Lateral", False), 
        ("Crunch en Polea Alta", True), ("Deadbug", False), ("Mountain Climbers", False)
    ]
}

NIVELES = ["Novato", "Intermedio", "Pro"]
OBJETIVOS = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Mantenimiento / Salud"]
GENEROS = ["Hombre", "Mujer"]
MESES = range(1, 7)
SEMANAS = range(1, 5)

def get_weekly_stats(semana, base_series, objetivo):
    """
    Define la Sobrecarga Progresiva segun la semana del mes.
    1: Intro (Carga base)
    2: Volumen (Mas series)
    3: Intensidad (Menos reps, mas peso/fuerza)
    4: Deload (Descarga tecnica, menos volumen)
    """
    if semana == 1:
        return base_series, "10-12", 90
    elif semana == 2:
        return base_series + 1, "10-12", 90 # Pico de Volumen
    elif semana == 3:
        return base_series, "6-8", 120 # Pico de Intensidad (Fuerza)
    else: # Deload
        return max(2, base_series - 1), "12-15", 60 # Descarga activa

def generate_routine():
    total_data = []
    print("🚀 Generando Entrenamiento de Élite con Sobrecarga Progresiva...")
    
    for nivel in NIVELES:
        for objetivo in OBJETIVOS:
            for genero in GENEROS:
                for mes in MESES:
                    # Dificultad base por nivel
                    base_series = {"Novato": 3, "Intermedio": 4, "Pro": 5}[nivel]
                    if mes > 3: base_series += 1 
                    
                    for semana in SEMANAS:
                        # Obtener modulacion de la semana
                        final_series, reps, descanso = get_weekly_stats(semana, base_series, objetivo)
                        
                        # Ajuste fino por objetivo (Override reps si es definicion)
                        if objetivo == "Definición / Quema de Grasa" and semana != 3:
                            reps = "12-15"

                        for dia in range(1, 6):
                            # Seleccion de Pool segun split estricto
                            if dia == 1: pool_key = "SUPERIOR_PUSH"
                            elif dia == 2: pool_key = "SUPERIOR_PULL"
                            elif dia == 3: pool_key = "INFERIOR_CUAD"
                            elif dia == 4: pool_key = "INFERIOR_POSTERIOR"
                            else: pool_key = "CORE_MIX"
                            
                            all_exs = EX_POOLS[pool_key]
                            
                            # FILTRADO INTELIGENTE POR NIVEL
                            if nivel == "Novato":
                                # Novatos: 70% maquinas/poleas, 30% libres basicos
                                selected_pool = [ex[0] for ex in all_exs if ex[1] or "Barra" not in ex[0]]
                                num_ex = 4
                            elif nivel == "Intermedio":
                                selected_pool = [ex[0] for ex in all_exs]
                                num_ex = 6
                            else: # PRO
                                # Pro: Enfoque en pesos libres pesados y volumen alto
                                selected_pool = [ex[0] for ex in all_exs if not ex[1] or "Dominadas" in ex[0] or "Fondos" in ex[0]]
                                # Fallback si el pool pro es muy chico
                                if len(selected_pool) < 5: selected_pool = [ex[0] for ex in all_exs]
                                num_ex = 7

                            # Ajuste de volumen por genero
                            vol_series = final_series
                            if genero == "Mujer":
                                if dia in [1, 2]: vol_series = max(2, final_series - 1)
                                if dia in [3, 4]: vol_series = final_series + 1

                            # Seleccion final de ejercicios (Rotacion por semana)
                            start_idx = (semana - 1) % (len(selected_pool) - num_ex + 1) if len(selected_pool) > num_ex else 0
                            exercises = selected_pool[start_idx : start_idx + num_ex]
                            
                            for ex_name in exercises:
                                total_data.append({
                                    "nombre": ex_name,
                                    "series": vol_series,
                                    "reps": reps,
                                    "descanso": descanso,
                                    "genero": genero,
                                    "nivel": nivel,
                                    "mes": mes,
                                    "dia": dia,
                                    "objetivo": objetivo,
                                    "semana": semana
                                })
                                
    return total_data

def seed_db():
    data = generate_routine()
    total = len(data)
    print(f"📦 Total de registros generados: {total}")
    
    print("🧹 Limpiando base de datos para inyectar Elite v2...")
    try:
        supabase.table("ejercicios").delete().neq("id", 0).execute()
    except: pass
    
    batch_size = 500
    for i in range(0, total, batch_size):
        batch = data[i:i + batch_size]
        try:
            supabase.table("ejercicios").insert(batch).execute()
            print(f"✅ Lote {i // batch_size + 1} sincronizado.")
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    start = time.time()
    seed_db()
    print(f"✨ ¡Sistema de Entrenamiento de Élite desplegado en {round(time.time() - start, 2)}s!")
