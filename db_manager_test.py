import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from models import User, Exercise, Diet, WeightHistory, WorkoutLog, HydrationLog, PRLog
from services.image_service import get_exercise_image
from supabase_config import create_custom_client

# Cargar variables de entorno de forma dinamica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Carga de credenciales desde el entorno
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Error: No se encontraron las variables de entorno SUPABASE_URL o SUPABASE_KEY")

# Inicializacion del cliente de Supabase
def get_supabase_client():
    return create_custom_client(url, key)

def login_user(client, email, password):
    return client.auth.sign_in_with_password({"email": email, "password": password})

def logout_user(client):
    try:
        client.auth.sign_out()
        return True
    except:
        return False
