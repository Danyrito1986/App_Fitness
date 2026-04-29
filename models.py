from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    id: int
    nombre: str
    objetivo: str
    peso_actual: float
    genero: str = "Hombre"
    nivel: str = "Novato"
    altura: float = 170.0
    cuello: float = 40.0
    cintura: float = 85.0
    cadera: float = 90.0
    pecho: float = 100.0
    gluteo: float = 95.0
    bicep: float = 35.0
    muslo: float = 55.0
    edad: int = 25
    mes_actual: int = 1
    entrenos_mes: int = 0

    def get_macros(self):
        """Calcula calorías y macros usando Katch-McArdle y la Marina."""
        import math
        # 1. Grasa Corporal (Marina)
        if self.genero == "Hombre":
            diff = max(1, self.cintura - self.cuello)
            bf = 495 / (1.0324 - 0.19077 * math.log10(diff) + 0.15456 * math.log10(self.altura)) - 450
        else:
            suma = max(1, self.cintura + self.cadera - self.cuello)
            bf = 495 / (1.29579 - 0.35004 * math.log10(suma) + 0.22100 * math.log10(self.altura)) - 450
        
        bf = max(5, bf)
        masa_magra = self.peso_actual * (1 - (bf / 100))
        
        # 2. TMB (Katch-McArdle) y GET (Gasto Energético Total)
        tmb = 370 + (21.6 * masa_magra)
        get = tmb * 1.55  # Multiplicador de actividad moderada
        
        # 3. Ajuste por objetivo
        ajuste = 0
        if self.objetivo == "Aumento de masa muscular":
            ajuste = 400
            p_multiplier, f_multiplier = 2.0, 0.8
        elif self.objetivo == "Definición / Quema de Grasa":
            ajuste = -500
            p_multiplier, f_multiplier = 2.4, 0.7
        else:
            ajuste = 0
            p_multiplier, f_multiplier = 1.8, 0.8
            
        cal_total = get + ajuste
        prot = self.peso_actual * p_multiplier
        fat = self.peso_actual * f_multiplier
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

@dataclass
class Exercise:
    id: int
    nombre: str
    series: int
    reps: int
    rutina_id: int
    descanso: int = 60 # Tiempo de descanso en segundos

@dataclass
class Diet:
    id: int
    tiempo: str
    cal: int
    comida: str
    p: int
    c: int
    g: int

@dataclass
class WeightHistory:
    usuario_id: int
    peso: float
    fecha: str

@dataclass
class WorkoutLog:
    usuario_id: int
    rutina_nombre: str
    fecha: str

@dataclass
class HydrationLog:
    usuario_id: int
    vasos: int
    fecha: str

@dataclass
class PRLog:
    usuario_id: int
    ejercicio_nombre: str
    peso: float
    fecha: str
