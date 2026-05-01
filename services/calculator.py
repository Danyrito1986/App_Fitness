import math
from models import User

def calculate_macros(user: User):
    """Calcula calorías y macros usando Katch-McArdle y la Marina."""
    
    # 1. Grasa Corporal (Marina)
    if user.genero == "Hombre":
        diff = max(1, user.cintura - user.cuello)
        bf = 495 / (1.0324 - 0.19077 * math.log10(diff) + 0.15456 * math.log10(user.altura)) - 450
    else:
        suma = max(1, user.cintura + user.cadera - user.cuello)
        bf = 495 / (1.29579 - 0.35004 * math.log10(suma) + 0.22100 * math.log10(user.altura)) - 450
    
    bf = max(5, bf)
    masa_magra = user.peso_actual * (1 - (bf / 100))
    
    # 2. TMB (Katch-McArdle) y GET (Gasto Energético Total)
    tmb = 370 + (21.6 * masa_magra)
    get = tmb * 1.55  # Multiplicador de actividad moderada
    
    # 3. Ajuste por objetivo
    ajuste = 0
    if user.objetivo == "Aumento de masa muscular":
        ajuste = 400
        p_multiplier, f_multiplier = 2.0, 0.8
    elif user.objetivo == "Definición / Quema de Grasa":
        ajuste = -500
        p_multiplier, f_multiplier = 2.4, 0.7
    else:
        ajuste = 0
        p_multiplier, f_multiplier = 1.8, 0.8
        
    cal_total = get + ajuste
    prot = user.peso_actual * p_multiplier
    fat = user.peso_actual * f_multiplier
    carb = (cal_total - (prot * 4) - (fat * 9)) / 4
    
    return {
        "cal": int(cal_total),
        "tdee": int(get),
        "ajuste": ajuste,
        "p": int(prot),
        "c": int(carb),
        "f": int(fat),
        "bf": round(bf, 1),
        "masa_magra": round(masa_magra, 1)
    }
