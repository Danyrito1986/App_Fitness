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
def get_supabase_client() -> Client:
    """Crea una nueva instancia del cliente de Supabase para cada sesión."""
    return create_custom_client(url, key)

def login_user(client: Client, email: str, password: str):
    """Inicia sesión con email y contraseña."""
    return client.auth.sign_in_with_password({"email": email, "password": password})

def logout_user(client: Client):
    """Cierra la sesión del usuario."""
    try:
        client.auth.sign_out()
        return True
    except:
        return False

def register_user(client: Client, email: str, password: str, nombre: str):
    """Registra un nuevo usuario y crea su perfil en la tabla 'usuarios'."""
    # 1. Crear usuario en Supabase Auth
    auth_response = client.auth.sign_up({"email": email, "password": password})
    
    if auth_response.user:
        # 2. Intentar crear perfil en la tabla 'usuarios'
        profile_data = {"nombre": nombre, "objetivo": "Ganar masa muscular", "peso_actual": 0.0, "email": email}
        client.table("usuarios").insert(profile_data).execute()
    
    return auth_response

def get_user(client: Client) -> User:
    """Obtiene el perfil del usuario vinculado a su sesión de Auth."""
    try:
        auth_response = client.auth.get_user()
        
        if not auth_response or not auth_response.user:
            return None
            
        email = auth_response.user.email
        
        # 1. Buscar perfil vinculado por el email
        response = client.table("usuarios").select("*").eq("email", email).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            u_data = response.data[0]
            return User(
                id=u_data["id"], 
                nombre=u_data.get("nombre") or "Usuario", 
                objetivo=u_data.get("objetivo") or "Aumento de masa muscular", 
                peso_actual=float(u_data.get("peso_actual") or 0.0),
                genero=u_data.get("genero") or "Hombre",
                nivel=u_data.get("nivel") or "Novato",
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
        
        # 2. Si no existe, crearlo vinculado permanentemente al email de Auth
        new_profile = {
            "email": email,
            "nombre": email.split("@")[0],
            "objetivo": "Aumento de masa muscular",
            "peso_actual": 0.0,
            "genero": "Hombre",
            "nivel": "Novato"
        }
        
        res = client.table("usuarios").insert(new_profile).execute()
        if res.data:
            u_data = res.data[0]
            return User(
                id=u_data["id"], 
                nombre=u_data["nombre"], 
                objetivo=u_data["objetivo"], 
                peso_actual=0.0
            )

    except Exception as e:
        print(f"DEBUG: Error crítico en get_user: {e}")
    return None

def update_user_profile(client: Client, user_id: int, data: dict) -> bool:
    """Actualiza los datos del perfil de forma segura."""
    try:
        mapping = {
            "nombre": "nombre",
            "objetivo": "objetivo",
            "peso": "peso_actual",
            "genero": "genero",
            "nivel": "nivel",
            "altura": "altura",
            "cuello": "cuello",
            "cintura": "cintura",
            "cadera": "cadera",
            "pecho": "pecho",
            "gluteo": "gluteo",
            "bicep": "bicep",
            "muslo": "muslo",
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

        res = client.table("usuarios").update(update_data).eq("id", user_id).execute()
        return len(res.data) > 0
    except Exception as e:
        print(f"DEBUG: Error en update_user_profile: {e}")
        return False

def get_routines(client: Client):
    """Retorna una lista de tuplas (id, nombre) de todas las rutinas."""
    try:
        response = client.table("rutinas").select("id, nombre").execute()
        return [(r["id"], r["nombre"]) for r in response.data]
    except:
        return []

def get_dynamic_exercises(client: Client, genero: str, nivel: str, mes: int, dia: int, objetivo: str, semana: int = 1) -> list[Exercise]:
    """Obtiene los ejercicios filtrados por mes, semana y día."""
    try:
        query = client.table("ejercicios")\
            .select("*")\
            .eq("genero", genero)\
            .eq("nivel", nivel)\
            .eq("mes", mes)\
            .eq("dia", dia)\
            .eq("objetivo", objetivo)
        
        # Filtrar por semana si existe la columna en la tabla
        # Si no existe, Supabase ignorará el filtro o devolverá error que manejaremos
        try:
            query = query.eq("semana", semana)
        except:
            pass

        response = query.execute()
        
        if not response.data:
            # Fallback sin objetivo si no hay resultados específicos
            response = client.table("ejercicios")\
                .select("*")\
                .eq("genero", genero)\
                .eq("nivel", nivel)\
                .eq("mes", mes)\
                .eq("dia", dia)\
                .execute()

        if not response.data:
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
        print(f"DEBUG_PRO: Error en get_dynamic_exercises: {e}")
        return []

def get_dietas(client: Client) -> list[Diet]:
    """Obtiene el plan nutricional completo."""
    try:
        response = client.table("dietas").select("*").execute()
        return [Diet(id=d["id"], tiempo=d["tiempo"], cal=d["cal"], comida=d["comida"], p=d["p"], c=d["c"], g=d["g"]) for d in response.data]
    except:
        return []

def log_workout(client: Client, user_id: int, routine_name: str) -> bool:
    """Registra la finalizacion de un entrenamiento."""
    try:
        client.table("historial_entrenos").insert({"usuario_id": user_id, "rutina_nombre": routine_name}).execute()
        return True
    except: 
        return False

def log_weight(client: Client, user_id: int, weight: float) -> bool:
    """Registra un nuevo pesaje."""
    try:
        client.table("historial_peso").insert({"usuario_id": user_id, "peso": weight}).execute()
        return True
    except: 
        return False

def get_weight_history(client: Client, user_id: int) -> list[WeightHistory]:
    """Obtiene el historial de peso."""
    try:
        response = client.table("historial_peso").select("peso, fecha").eq("usuario_id", user_id).order("fecha").execute()
        return [WeightHistory(usuario_id=user_id, peso=r["peso"], fecha=r["fecha"]) for r in response.data]
    except:
        return []

def get_workout_stats(client: Client, user_id: int) -> int:
    """Cuenta el numero total de entrenamientos."""
    try:
        response = client.table("historial_entrenos").select("*", count="exact").eq("usuario_id", user_id).execute()
        return response.count if response.count is not None else 0
    except:
        return 0

def log_water(client: Client, user_id: int, cups: int) -> bool:
    """Registra vasos de agua."""
    try:
        client.table("historial_agua").insert({"usuario_id": user_id, "vasos": cups}).execute()
        return True
    except Exception as e:
        print(f"Error log_water: {e}")
        return False

def get_daily_water(client: Client, user_id: int) -> int:
    """Obtiene total de agua hoy."""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        response = client.table("historial_agua").select("vasos").eq("usuario_id", user_id).gte("fecha", today).execute()
        return sum(r["vasos"] for r in response.data) if response.data else 0
    except:
        return 0

def log_pr(client: Client, user_id: int, exercise: str, weight: float) -> bool:
    """Registra un Record Personal."""
    try:
        client.table("records_fuerza").insert({"usuario_id": user_id, "ejercicio_nombre": exercise, "peso": weight}).execute()
        return True
    except Exception as e:
        print(f"Error log_pr: {e}")
        return False

def get_prs(client: Client, user_id: int):
    """Obtiene los records de fuerza."""
    try:
        response = client.table("records_fuerza").select("*").eq("usuario_id", user_id).order("fecha", desc=True).execute()
        return [PRLog(usuario_id=r["usuario_id"], ejercicio_nombre=r["ejercicio_nombre"], peso=r["peso"], fecha=r["fecha"]) for r in response.data]
    except:
        return []

def get_last_weight(client: Client, user_id: int, exercise_name: str) -> float:
    """Obtiene el peso más reciente registrado."""
    try:
        response = client.table("records_fuerza")\
            .select("peso")\
            .eq("usuario_id", user_id)\
            .eq("ejercicio_nombre", exercise_name)\
            .order("fecha", desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            return float(response.data[0]["peso"])
        return 0.0
    except Exception as e:
        print(f"Error en get_last_weight: {e}")
        return 0.0

def save_workout_progress(client: Client, user_id: int, fecha: str, datos: dict) -> bool:
    """Guarda o actualiza el estado de las series completadas en JSONB."""
    try:
        # Usar upsert para actualizar si ya existe un registro para ese usuario y fecha
        client.table("progreso_series").upsert({
            "usuario_id": user_id,
            "fecha": fecha,
            "datos": datos
        }, on_conflict="usuario_id,fecha").execute()
        return True
    except Exception as e:
        print(f"Error save_workout_progress: {e}")
        return False

def get_workout_progress(client: Client, user_id: int, fecha: str) -> dict:
    """Recupera el estado de las series completadas de la base de datos."""
    try:
        response = client.table("progreso_series").select("datos").eq("usuario_id", user_id).eq("fecha", fecha).execute()
        if response.data:
            return response.data[0]["datos"]
        return {}
    except Exception as e:
        print(f"Error get_workout_progress: {e}")
        return {}
