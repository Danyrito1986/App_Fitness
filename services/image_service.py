import os

# Base URL del repositorio profesional de ejercicios (Public Domain)
RAW_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"

# Mapeo Técnico Curado: Nombre en App -> ID del Repositorio Profesional
# Se prefiere la imagen '0.jpg' (inicio) o '1.jpg' (ejecución/pico)
TECHNICAL_MAPPING = {
    # --- DÍA 1: EMPUJE SUPERIOR ---
    "Press de Banca con Barra": "Barbell_Bench_Press_-_Medium_Grip/1.jpg",
    "Press Militar con Barra": "Barbell_Shoulder_Press/1.jpg",
    "Aperturas con Mancuernas (Flat)": "Dumbbell_Flyes/1.jpg",
    "Elevaciones Laterales (Polea/Mancuerna)": "Side_Lateral_Raise/1.jpg",
    "Press Francés con Barra Z": "EZ-Bar_Skullcrusher/1.jpg",
    "Fondos en Paralelas": "Dips_-_Chest_Version/1.jpg",

    # --- DÍA 2: JALÓN SUPERIOR ---
    "Dominadas Pronas": "Pullups/1.jpg",
    "Remo con Barra (Pendlay)": "Bent_Over_Barbell_Row/1.jpg",
    "Jalón al Pecho Agarre Estrecho": "Close-Grip_Front_Lat_Pulldown/1.jpg",
    "Pájaros con Mancuernas": "Dumbbell_Lying_Rear_Lateral_Raise/1.jpg",
    "Curl Martillo con Mancuernas": "Hammer_Curls/1.jpg",
    "Curl con Barra Z (Predicador)": "Preacher_Curl/1.jpg",

    # --- DÍA 3: EMPUJE INFERIOR ---
    "Sentadilla Trasera con Barra": "Barbell_Squat/1.jpg",
    "Prensa de Piernas (Pies Bajos)": "Leg_Press/1.jpg",
    "Zancadas Búlgaras": "Split_Squats/1.jpg",
    "Extensiones de Cuádriceps (Máquina)": "Leg_Extensions/1.jpg",
    "Elevación de Talones De Pie": "Standing_Calf_Raises/1.jpg",
    "Sissy Squat (Cuerpo/Peso)": "Weighted_Sissy_Squat/1.jpg",

    # --- DÍA 4: JALÓN INFERIOR ---
    "Peso Muerto Rumano (RDL)": "Romanian_Deadlift/1.jpg",
    "Hip Thrust con Barra": "Barbell_Hip_Thrust/1.jpg",
    "Curl de Pierna Acostado": "Lying_Leg_Curls/1.jpg",
    "Kettlebell Swings (o Pull-through)": "One-Arm_Kettlebell_Swings/1.jpg",
    "Abducciones en Máquina (Glúteo Medio)": "Thigh_Abductor/1.jpg",
    "Patada de Glúteo en Polea": "Glute_Kickback/1.jpg",

    # --- DÍA 5: CORE ---
    "Rueda Abdominal (Rollouts)": "Ab_Roller/1.jpg",
    "Press Pallof (Polea/Banda)": "Pallof_Press/1.jpg",
    "Elevación de Piernas (Colgado)": "Hanging_Leg_Raise/1.jpg",
    "Plancha Lateral con Elevación": "Side_Bridge/1.jpg",
    "Facepulls (Salud de Manguito)": "Face_Pull/1.jpg",
    "Deadbug Pro (Control Lumbar)": "Dead_Bug/1.jpg",
}

def get_exercise_image(exercise_name: str) -> str:
    """
    Retorna la URL de la imagen técnica exacta del ejercicio.
    Utiliza un mapeo profesional 1 a 1.
    """
    # 1. Coincidencia exacta en mapeo técnico
    if exercise_name in TECHNICAL_MAPPING:
        return RAW_BASE_URL + TECHNICAL_MAPPING[exercise_name]

    # 2. Lógica de búsqueda inteligente por palabras clave si no hay match exacto
    name_lower = exercise_name.lower()
    
    keywords = {
        "press": "Barbell_Bench_Press_-_Medium_Grip/1.jpg",
        "sentadilla": "Barbell_Squat/1.jpg",
        "squat": "Barbell_Squat/1.jpg",
        "curl": "Dumbbell_Alternate_Bicep_Curl/1.jpg",
        "rem": "Bent_Over_Barbell_Row/1.jpg",
        "ab": "Ab_Roller/1.jpg",
        "core": "Plank/1.jpg",
        "pierna": "Leg_Press/1.jpg",
        "hombro": "Barbell_Shoulder_Press/1.jpg",
        "glute": "Glute_Kickback/1.jpg"
    }

    for key, path in keywords.items():
        if key in name_lower:
            return RAW_BASE_URL + path

    # 3. Fallback: Imagen de gimnasio genérica de alta calidad (Unsplash)
    return "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop"
