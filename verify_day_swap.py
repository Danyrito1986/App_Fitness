import os
from dotenv import load_dotenv
from seed_v4_pure_splits import seed_pure_splits_v4

def verify_swap():
    """Verifica localmente que el intercambio de días 2 y 3 se realizó correctamente."""
    print("\n🔍 VERIFICANDO INTERCAMBIO DE DÍAS (D2 <-> D3)...")
    
    # Generar ejercicios (modo previsualización)
    ejercicios = seed_pure_splits_v4(execute_insert=False)
    
    # Filtrar un perfil específico para la muestra
    muestra_d2 = [e["nombre"] for e in ejercicios if e["mes"] == 1 and e["semana"] == 1 and e["dia"] == 2 and e["genero"] == "Hombre" and e["nivel"] == "Pro"]
    muestra_d3 = [e["nombre"] for e in ejercicios if e["mes"] == 1 and e["semana"] == 1 and e["dia"] == 3 and e["genero"] == "Hombre" and e["nivel"] == "Pro"]

    print(f"\n📅 DÍA 2 (Ahora debe ser Pierna/Push):")
    for ex in muestra_d2: print(f"   - {ex}")
    
    print(f"\n📅 DÍA 3 (Ahora debe ser Jalón Superior/Pull):")
    for ex in muestra_d3: print(f"   - {ex}")

    # Validaciones automáticas
    is_d2_ok = any("Sentadilla" in n or "Prensa" in n for n in muestra_d2)
    is_d3_ok = any("Dominadas" in n or "Remo" in n for n in muestra_d3)

    if is_d2_ok and is_d3_ok:
        print("\n✅ INTERCAMBIO CONFIRMADO TÉCNICAMENTE.")
    else:
        print("\n❌ ERROR: El intercambio no parece correcto.")

if __name__ == "__main__":
    verify_swap()
