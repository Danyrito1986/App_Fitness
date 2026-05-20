import os

# Base URL del repositorio profesional de ejercicios (Public Domain)
RAW_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"

# Mapeo Técnico Curado: Nombre en App -> ID del Repositorio Profesional
# Se sincroniza con los nombres de seed_rutinas_pro.py
TECHNICAL_MAPPING = {
    # --- SUPERIOR PUSH ---
    "Press de Banca con Barra": "Barbell_Bench_Press_-_Medium_Grip/1.jpg",
    "Press Militar con Barra": "Barbell_Shoulder_Press/1.jpg",
    "Aperturas con Mancuernas": "Dumbbell_Flyes/1.jpg",
    "Elevaciones Laterales": "Side_Lateral_Raise/1.jpg",
    "Press Frances": "EZ-Bar_Skullcrusher/1.jpg",
    "Fondos en Paralelas": "Dips_-_Chest_Version/1.jpg",
    "Press Inclinado con Mancuernas": "Incline_Dumbbell_Press/1.jpg",
    "Cruce de Poleas": "Cable_Cross-over/1.jpg",

    # --- SUPERIOR PULL ---
    "Dominadas Pronas": "Pullups/1.jpg",
    "Remo con Barra": "Bent_Over_Barbell_Row/1.jpg",
    "Jalon al Pecho": "Lat_Pulldown/1.jpg",
    "Pajaros con Mancuernas": "Dumbbell_Lying_Rear_Lateral_Raise/1.jpg",
    "Curl Martillo": "Hammer_Curls/1.jpg",
    "Curl con Barra Z": "Preacher_Curl/1.jpg",
    "Remo en Polea Baja": "Seated_Cable_Rows/1.jpg",
    "Facepulls": "Face_Pull/1.jpg",

    # --- INFERIOR CUAD ---
    "Sentadilla Trasera": "Barbell_Squat/1.jpg",
    "Prensa de Piernas": "Leg_Press/1.jpg",
    "Zancadas Bulgaras": "Split_Squats/1.jpg",
    "Extensiones de Cuadriceps": "Leg_Extensions/1.jpg",
    "Sissy Squat": "Weighted_Sissy_Squat/1.jpg",
    "Hack Squat": "Hack_Squat/1.jpg",
    "Sentadilla Goblet": "Goblet_Squat/1.jpg",

    # --- INFERIOR POSTERIOR ---
    "Peso Muerto Rumano": "Romanian_Deadlift/1.jpg",
    "Hip Thrust con Barra": "Barbell_Hip_Thrust/1.jpg",
    "Curl de Pierna Acostado": "Lying_Leg_Curls/1.jpg",
    "Kettlebell Swings": "One-Arm_Kettlebell_Swings/1.jpg",
    "Abducciones en Maquina": "Thigh_Abductor/1.jpg",
    "Patada de Gluteo": "Glute_Kickback/1.jpg",
    "Peso Muerto Sumo": "Sumo_Deadlift/1.jpg",

    # --- CORE ---
    "Rueda Abdominal": "Ab_Roller/1.jpg",
    "Elevacion de Piernas": "Hanging_Leg_Raise/1.jpg",
    "Press Pallof": "Pallof_Press/1.jpg",
    "Plancha Lateral": "Side_Bridge/1.jpg",
    "Crunch en Polea Alta": "Ab_Crunch_Machine/1.jpg",
    "Deadbug": "Dead_Bug/1.jpg",
    "Mountain Climbers": "Mountain_Climbers/1.jpg"
}

def get_exercise_image(exercise_name: str) -> str:
    """
    Retorna la URL de la imagen técnica exacta del ejercicio.
    Utiliza un mapeo profesional 1 a 1 sincronizado con la base de datos.
    """
    # 1. Coincidencia exacta en mapeo técnico
    if exercise_name in TECHNICAL_MAPPING:
        return RAW_BASE_URL + TECHNICAL_MAPPING[exercise_name]

    # 2. Lógica de búsqueda inteligente por palabras clave (Más específica para evitar errores)
    name_lower = exercise_name.lower()
    
    if "banca" in name_lower or "bench" in name_lower: return RAW_BASE_URL + "Barbell_Bench_Press_-_Medium_Grip/1.jpg"
    if "militar" in name_lower: return RAW_BASE_URL + "Barbell_Shoulder_Press/1.jpg"
    if "sentadilla" in name_lower or "squat" in name_lower: return RAW_BASE_URL + "Barbell_Squat/1.jpg"
    if "prensa" in name_lower: return RAW_BASE_URL + "Leg_Press/1.jpg"
    if "muerto" in name_lower: return RAW_BASE_URL + "Romanian_Deadlift/1.jpg"
    if "curl" in name_lower: return RAW_BASE_URL + "Dumbbell_Alternate_Bicep_Curl/1.jpg"
    if "remo" in name_lower: return RAW_BASE_URL + "Bent_Over_Barbell_Row/1.jpg"
    if "abdominal" in name_lower or "crunch" in name_lower: return RAW_BASE_URL + "Ab_Roller/1.jpg"
    if "glute" in name_lower: return RAW_BASE_URL + "Glute_Kickback/1.jpg"
    if "tricep" in name_lower or "frances" in name_lower: return RAW_BASE_URL + "EZ-Bar_Skullcrusher/1.jpg"

    # 3. Fallback: Imagen de gimnasio genérica de alta calidad (Unsplash)
    return "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop"
