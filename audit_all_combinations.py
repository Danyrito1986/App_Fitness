import db_manager as db
from supabase import Client

def check_all_combinations():
    client = db.get_supabase_client()
    
    objetivos = ["Aumento de masa muscular", "Definición / Quema de Grasa", "Resistencia"]
    niveles = ["Novato", "Intermedio", "Avanzado"]
    generos = ["Hombre", "Mujer"]
    
    print("--- Auditoría de Disponibilidad de Ejercicios ---")
    
    for gen in generos:
        for niv in niveles:
            for obj in objetivos:
                # Probar Mes 1, Semana 1, Día 1 como muestra
                res = client.table("ejercicios").select("id", count="exact")\
                    .eq("genero", gen)\
                    .eq("nivel", niv)\
                    .eq("objetivo", obj)\
                    .eq("mes", 1)\
                    .eq("dia", 1)\
                    .execute()
                
                count = res.count if res.count is not None else 0
                status = "✅ OK" if count > 0 else "❌ VACÍO"
                print(f"[{status}] {gen} | {niv} | {obj} -> {count} ejercicios")

if __name__ == "__main__":
    check_all_combinations()
