import db_manager as db
from supabase import Client

def check_user_filters():
    client = db.get_supabase_client()
    user = db.get_user(client)
    
    if not user:
        print("No se encontró usuario logueado.")
        return

    print(f"--- Datos del Usuario ---")
    print(f"ID: {user.id}")
    print(f"Objetivo: {user.objetivo}")
    print(f"Género: {user.genero}")
    print(f"Nivel: {user.nivel}")
    print(f"Mes Actual: {user.mes_actual}")
    print(f"Entrenos Mes: {user.entrenos_mes}")
    
    semana = (user.entrenos_mes // 5) % 4 + 1
    dia = (user.entrenos_mes % 5) + 1
    
    print(f"\n--- Filtros que aplicará la App ---")
    print(f"Mes: {user.mes_actual}")
    print(f"Semana: {semana}")
    print(f"Día: {dia}")
    
    print(f"\n--- Buscando ejercicios en Supabase con estos filtros ---")
    res = client.table("ejercicios").select("*")\
        .eq("genero", user.genero)\
        .eq("nivel", user.nivel)\
        .eq("mes", user.mes_actual)\
        .eq("dia", dia)\
        .eq("objetivo", user.objetivo)\
        .eq("semana", semana)\
        .execute()
    
    print(f"Ejercicios encontrados: {len(res.data)}")
    for ex in res.data:
        print(f"- {ex['nombre']} (ID: {ex['id']})")
        
    if len(res.data) == 0:
        print("\n¡ALERTA! No se encontraron ejercicios para esta combinación de filtros.")
        print("Probando sin filtro de semana...")
        res_no_sem = client.table("ejercicios").select("*")\
            .eq("genero", user.genero)\
            .eq("nivel", user.nivel)\
            .eq("mes", user.mes_actual)\
            .eq("dia", dia)\
            .eq("objetivo", user.objetivo)\
            .execute()
        print(f"Ejercicios encontrados sin filtro de semana: {len(res_no_sem.data)}")

if __name__ == "__main__":
    check_user_filters()
