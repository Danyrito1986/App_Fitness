import db_manager as db
from supabase import Client

def count_all_exercises():
    client = db.get_supabase_client()
    try:
        res = client.table("ejercicios").select("id", count="exact").execute()
        total = res.count
        print(f"Total de ejercicios en la tabla: {total}")
        
        # Conteo por objetivo
        obj_res = client.table("ejercicios").select("objetivo").execute()
        counts = {}
        for row in obj_res.data:
            obj = row['objetivo']
            counts[obj] = counts.get(obj, 0) + 1
        
        print("\nDistribución por objetivo:")
        for obj, count in counts.items():
            print(f"- {obj}: {count}")
            
        # Conteo por género
        gen_res = client.table("ejercicios").select("genero").execute()
        g_counts = {}
        for row in gen_res.data:
            g = row['genero']
            g_counts[g] = g_counts.get(g, 0) + 1
        
        print("\nDistribución por género:")
        for g, g_count in g_counts.items():
            print(f"- {g}: {g_count}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    count_all_exercises()
