import os

# Diccionario curado de imágenes de alta fidelidad para ejercicios específicos
# Fuente: IDs de Unsplash/Pexels verificados para Fitness Profesional
EXERCISE_IMAGES = {
    # --- EMPUJE SUPERIOR ---
    "Press de Banca con Barra": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?q=80&w=600&auto=format&fit=crop",
    "Press Militar con Barra": "https://images.unsplash.com/photo-1532384661798-58b53a4fbe37?q=80&w=600&auto=format&fit=crop",
    "Aperturas con Mancuernas (Flat)": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=600&auto=format&fit=crop",
    "Elevaciones Laterales (Polea/Mancuerna)": "https://images.unsplash.com/photo-1593164841883-ef48e89146ec?q=80&w=600&auto=format&fit=crop",
    "Press Francés con Barra Z": "https://images.unsplash.com/photo-1620188467120-5042ed1eb5da?q=80&w=600&auto=format&fit=crop",
    "Fondos en Paralelas": "https://images.unsplash.com/photo-1590487988256-9ed24133863e?q=80&w=600&auto=format&fit=crop",

    # --- JALÓN SUPERIOR ---
    "Dominadas Pronas": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?q=80&w=600&auto=format&fit=crop",
    "Remo con Barra (Pendlay)": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=600&auto=format&fit=crop",
    "Jalón al Pecho Agarre Estrecho": "https://images.unsplash.com/photo-1591940742878-13aba4b7a35e?q=80&w=600&auto=format&fit=crop",
    "Pájaros con Mancuernas": "https://images.unsplash.com/photo-1590239098569-e611bb26eb39?q=80&w=600&auto=format&fit=crop",
    "Curl Martillo con Mancuernas": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=600&auto=format&fit=crop",
    "Curl con Barra Z (Predicador)": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=600&auto=format&fit=crop",

    # --- EMPUJE INFERIOR ---
    "Sentadilla Trasera con Barra": "https://images.unsplash.com/photo-1574673848896-4cc9fe5f200d?q=80&w=600&auto=format&fit=crop",
    "Prensa de Piernas (Pies Bajos)": "https://images.unsplash.com/photo-1597452485669-2c7bb5fef90d?q=80&w=600&auto=format&fit=crop",
    "Zancadas Búlgaras": "https://images.unsplash.com/photo-1507398941214-57f1bdb6f0bf?q=80&w=600&auto=format&fit=crop",
    "Extensiones de Cuádriceps (Máquina)": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop",
    "Elevación de Talones De Pie": "https://images.unsplash.com/photo-1434682881908-b43d0467b798?q=80&w=600&auto=format&fit=crop",

    # --- JALÓN INFERIOR ---
    "Peso Muerto Rumano (RDL)": "https://images.unsplash.com/photo-1567598508481-65985588e295?q=80&w=600&auto=format&fit=crop",
    "Hip Thrust con Barra": "https://images.unsplash.com/photo-1521804906057-1df8fdb718b7?q=80&w=600&auto=format&fit=crop",
    "Curl de Pierna Acostado": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?q=80&w=600&auto=format&fit=crop",

    # --- CORE ---
    "Rueda Abdominal (Rollouts)": "https://images.unsplash.com/photo-1637666505754-7416ebd70cbf?q=80&w=600&auto=format&fit=crop",
    "Elevación de Piernas (Colgado)": "https://images.unsplash.com/photo-1536922645426-5d658ab49b81?q=80&w=600&auto=format&fit=crop",
    "Facepulls (Salud de Manguito)": "https://images.unsplash.com/photo-1591940742878-13aba4b7a35e?q=80&w=600&auto=format&fit=crop",
}

def get_exercise_image(exercise_name: str) -> str:
    """
    Retorna una URL de imagen profesional curada para el ejercicio.
    Si no encuentra el ejercicio exacto, busca por palabras clave.
    """
    # 1. Intento por nombre exacto
    if exercise_name in EXERCISE_IMAGES:
        return EXERCISE_IMAGES[exercise_name]

    # 2. Intento por palabras clave inteligentes
    name_lower = exercise_name.lower()
    
    keywords = {
        "press": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?q=80&w=600&auto=format&fit=crop",
        "squat": "https://images.unsplash.com/photo-1574673848896-4cc9fe5f200d?q=80&w=600&auto=format&fit=crop",
        "sentadilla": "https://images.unsplash.com/photo-1574673848896-4cc9fe5f200d?q=80&w=600&auto=format&fit=crop",
        "curl": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=600&auto=format&fit=crop",
        "rem": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=600&auto=format&fit=crop",
        "ab": "https://images.unsplash.com/photo-1637666505754-7416ebd70cbf?q=80&w=600&auto=format&fit=crop",
        "core": "https://images.unsplash.com/photo-1637666505754-7416ebd70cbf?q=80&w=600&auto=format&fit=crop",
        "pierna": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop",
        "hombro": "https://images.unsplash.com/photo-1593164841883-ef48e89146ec?q=80&w=600&auto=format&fit=crop",
        "brazo": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=600&auto=format&fit=crop",
    }

    for key, url in keywords.items():
        if key in name_lower:
            return url

    # 3. Fallback final (Imagen de Gimnasio Premium)
    return "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop"
