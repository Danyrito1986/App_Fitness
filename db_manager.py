import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from models import User, Exercise, Diet, WeightHistory, WorkoutLog, HydrationLog, PRLog
from supabase_config import create_custom_client

# Cargar variables de entorno de forma dinámica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Carga de credenciales desde el entorno
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Error: No se encontraron las variables de entorno SUPABASE_URL o SUPABASE_KEY en el archivo .env")

# Inicializacion del cliente de Supabase optimizado para Render
supabase: Client = create_custom_client(url, key)

def login_user(email: str, password: str):
    """Inicia sesión con email y contraseña."""
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def register_user(email: str, password: str, nombre: str):
    """Registra un nuevo usuario y crea su perfil en la tabla 'usuarios'."""
    # 1. Crear usuario en Supabase Auth
    auth_response = supabase.auth.sign_up({"email": email, "password": password})
    
    if auth_response.user:
        # 2. Intentar crear perfil en la tabla 'usuarios' sin forzar el ID (dejar que sea autoincremental)
        profile_data = {"nombre": nombre, "objetivo": "Ganar masa muscular", "peso_actual": 0.0}
        
        # Intentamos detectar la columna de correo para vincularlo
        try:
            sample = supabase.table("usuarios").select("*").limit(1).execute()
            if sample.data:
                keys = sample.data[0].keys()
                if "correo" in keys: profile_data["correo"] = email
                elif "email" in keys: profile_data["email"] = email
        except:
            pass
            
        supabase.table("usuarios").insert(profile_data).execute()
    
    return auth_response

def get_user() -> User:
    """Obtiene el perfil del usuario actualmente autenticado vinculando Auth con la tabla 'usuarios'."""
    try:
        print("DEBUG: Intentando obtener usuario de Auth...")
        auth_response = supabase.auth.get_user()
        
        if not auth_response or not auth_response.user:
            print("DEBUG: No hay sesión activa en Supabase Auth.")
            return None
            
        email = auth_response.user.email
        print(f"DEBUG: Sesión activa para: {email}")
        
        # Intentamos buscar por correo o email directamente en Supabase
        for field in ["email", "correo"]:
            try:
                print(f"DEBUG: Buscando en tabla 'usuarios' por columna '{field}'...")
                response = supabase.table("usuarios").select("*").eq(field, email).limit(1).execute()
                
                if response.data and len(response.data) > 0:
                    u_data = response.data[0]
                    print(f"DEBUG: Perfil encontrado para {email}")
                    return User(
                        id=u_data["id"], 
                        nombre=u_data.get("nombre") or "Usuario", 
                        objetivo=u_data.get("objetivo") or "Aumento de masa muscular", 
                        peso_actual=float(u_data.get("peso_actual") or 0.0),
                        genero=u_data.get("genero") or "Hombre",
                        altura=float(u_data.get("altura") or 170.0),
                        cuello=float(u_data.get("cuello") or 40.0),
                        cintura=float(u_data.get("cintura") or 85.0),
                        cadera=float(u_data.get("cadera") or 90.0),
                        pecho=float(u_data.get("pecho") or 100.0),
                        gluteo=float(u_data.get("gluteo") or 95.0),
                        bicep=float(u_data.get("bicep") or 35.0),
                        muslo=float(u_data.get("muslo") or 55.0),
                        edad=int(u_data.get("edad") or 25),
                        mes_actual=int(u_data.get("mes_actual") or 1),
                        entrenos_mes=int(u_data.get("entrenos_mes") or 0)
                    )
            except Exception as e:
                print(f"DEBUG: Error buscando en columna '{field}': {e}")
                continue
        
        print(f"DEBUG: No se encontró ninguna fila en la tabla 'usuarios' vinculada al correo {email}")

    except Exception as e:
        print(f"DEBUG: Error crítico en get_user: {e}")
    return None

def update_user_profile(user_id: int, data: dict) -> bool:
    """Actualiza los datos del perfil de forma dinámica para evitar sobrescribir con valores por defecto."""
    try:
        auth_user = supabase.auth.get_user()
        if not auth_user or not auth_user.user:
            return False
            
        email = auth_user.user.email
        
        # Mapeo de nombres de campos del diccionario a nombres de columnas en DB
        # Esto asegura compatibilidad si los nombres difieren
        mapping = {
            "nombre": "nombre",
            "objetivo": "objetivo",
            "peso": "peso_actual",
            "genero": "genero",
            "altura": "altura",
            "cuello": "cuello",
            "cintura": "cintura",
            "cadera": "cadera",
            "edad": "edad",
            "mes_actual": "mes_actual",
            "entrenos_mes": "entrenos_mes"
        }
        
        update_data = {}
        for key, value in data.items():
            if key in mapping:
                update_data[mapping[key]] = value

        if not update_data:
            return False

        for field in ["email", "correo"]:
            try:
                res = supabase.table("usuarios").update(update_data).eq(field, email).execute()
                if res.data:
                    return True
            except:
                continue
        return False
    except Exception as e:
        print(f"Error update_user_profile: {e}")
        return False

def get_routines():
    """Retorna una lista de tuplas (id, nombre) de todas las rutinas."""
    try:
        response = supabase.table("rutinas").select("id, nombre").execute()
        return [(r["id"], r["nombre"]) for r in response.data]
    except:
        return []

def get_dynamic_exercises(genero: str, nivel: str, mes: int, dia: int) -> list[Exercise]:
    """
    Obtiene los ejercicios desde Supabase filtrados por género, nivel, mes y día.
    """
    try:
        # Corregido: Agregado el filtro de 'mes'
        response = supabase.table("ejercicios")\
            .select("*")\
            .eq("genero", genero)\
            .eq("nivel", nivel)\
            .eq("mes", mes)\
            .eq("dia", dia)\
            .execute()
        
        if not response.data:
            print(f"DEBUG: No se encontraron ejercicios para {genero}, {nivel}, Mes {mes}, Dia {dia}")
            return []
            
        return [
            Exercise(
                id=ej["id"], 
                nombre=ej["nombre"], 
                series=ej["series"], 
                reps=ej["reps"], 
                rutina_id=ej.get("rutina_id", 0),
                descanso=ej.get("descanso", 60)
            ) for ej in response.data
        ]
    except Exception as e:
        print(f"Error al traer ejercicios dinámicos: {e}")
        return []

def get_dietas() -> list[Diet]:
    """Obtiene el plan nutricional completo."""
    try:
        response = supabase.table("dietas").select("*").execute()
        return [
            Diet(
                id=d["id"], 
                tiempo=d["tiempo"], 
                cal=d["cal"], 
                comida=d["comida"], 
                p=d["p"], 
                c=d["c"], 
                g=d["g"]
            ) for d in response.data
        ]
    except:
        return []

def log_workout(user_id: int, routine_name: str) -> bool:
    """Registra la finalizacion de un entrenamiento en el historial."""
    try:
        supabase.table("historial_entrenos").insert({
            "usuario_id": user_id, 
            "rutina_nombre": routine_name
        }).execute()
        return True
    except: 
        return False

def log_weight(user_id: int, weight: float) -> bool:
    """Registra un nuevo pesaje en el historial de peso."""
    try:
        supabase.table("historial_peso").insert({
            "usuario_id": user_id, 
            "peso": weight
        }).execute()
        return True
    except: 
        return False

def get_weight_history(user_id: int) -> list[WeightHistory]:
    """Obtiene el historial de peso del usuario ordenado por fecha."""
    try:
        response = supabase.table("historial_peso").select("peso, fecha").eq("usuario_id", user_id).order("fecha").execute()
        return [
            WeightHistory(
                usuario_id=user_id, 
                peso=r["peso"], 
                fecha=r["fecha"]
            ) for r in response.data
        ]
    except:
        return []

def get_workout_stats(user_id: int) -> int:
    """Cuenta el numero total de entrenamientos realizados por el usuario."""
    try:
        response = supabase.table("historial_entrenos").select("*", count="exact").eq("usuario_id", user_id).execute()
        return response.count if response.count is not None else 0
    except:
        return 0

def log_water(user_id: int, cups: int) -> bool:
    """Registra vasos de agua con manejo de errores."""
    try:
        supabase.table("historial_agua").insert({"usuario_id": user_id, "vasos": cups}).execute()
        return True
    except Exception as e:
        print(f"Error log_water: {e}")
        return False

def get_daily_water(user_id: int) -> int:
    """Obtiene total de agua consumida hoy."""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        response = supabase.table("historial_agua").select("vasos").eq("usuario_id", user_id).gte("fecha", today).execute()
        return sum(r["vasos"] for r in response.data) if response.data else 0
    except:
        return 0

def log_pr(user_id: int, exercise: str, weight: float) -> bool:
    """Registra un Record Personal con manejo de errores."""
    try:
        supabase.table("records_fuerza").insert({"usuario_id": user_id, "ejercicio_nombre": exercise, "peso": weight}).execute()
        return True
    except Exception as e:
        print(f"Error log_pr: {e}")
        return False

def get_prs(user_id: int):
    """Obtiene los records de fuerza con manejo de errores."""
    try:
        response = supabase.table("records_fuerza").select("*").eq("usuario_id", user_id).order("fecha", desc=True).execute()
        return [PRLog(usuario_id=r["usuario_id"], ejercicio_nombre=r["ejercicio_nombre"], peso=r["peso"], fecha=r["fecha"]) for r in response.data]
    except:
        return []
