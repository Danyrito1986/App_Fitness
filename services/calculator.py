import math
from models import User

def calculate_macros(user: User):
    """Calcula calorías y macros usando Katch-McArdle y la Marina con validaciones robustas."""
    
    # 0. Validaciones de seguridad en inputs
    peso = max(10, user.peso_actual)
    altura = max(50, abs(user.altura))
    cintura = max(20, user.cintura)
    cuello = max(10, user.cuello)
    
    # 1. Grasa Corporal (Marina)
    try:
        if user.genero == "Hombre":
            diff = max(1, cintura - cuello)
            bf = 495 / (1.0324 - 0.19077 * math.log10(diff) + 0.15456 * math.log10(altura)) - 450
        else:
            cadera = max(20, user.cadera)
            suma = max(1, cintura + cadera - cuello)
            bf = 495 / (1.29579 - 0.35004 * math.log10(suma) + 0.22100 * math.log10(altura)) - 450
    except (ValueError, ZeroDivisionError):
        bf = 25.0 # Fallback seguro
    
    bf = max(5, min(60, bf)) # Limitar entre 5% y 60%
    masa_magra = peso * (1 - (bf / 100))
    
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
        
    cal_total = max(1200, get + ajuste) # Mínimo metabólico de seguridad
    prot = peso * p_multiplier
    fat = peso * f_multiplier
    carb = max(50, (cal_total - (prot * 4) - (fat * 9)) / 4)
    
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
