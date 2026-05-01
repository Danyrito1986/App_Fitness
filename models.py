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
