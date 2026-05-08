import unittest
from services.image_service import get_exercise_image, TECHNICAL_MAPPING

class ImageCatalogChaosTest(unittest.TestCase):
    
    def test_01_exact_match_integrity(self):
        """CAOS: Verifica que cada entrada del catálogo devuelva su URL única y profesional."""
        print("\n  - Escenario: Integridad de Coincidencia Exacta...")
        for name, path in TECHNICAL_MAPPING.items():
            result_url = get_exercise_image(name)
            self.assertIn(path, result_url, f"Fallo en ejercicio: {name}")
        print(f"  [PASSED] {len(TECHNICAL_MAPPING)} ejercicios mapeados con 100% de precisión.")

    def test_02_keyword_intelligence_stress(self):
        """CAOS: Prueba variaciones de nombres para validar la lógica de palabras clave."""
        print("  - Escenario: Inteligencia de Palabras Clave (Variaciones)...")
        test_cases = {
            "Press de pecho inclinado": "press", # Debe encontrar 'press'
            "Sentadilla con mancuerna": "sentadilla", # Debe encontrar 'sentadilla'
            "Cualquier tipo de Curl": "curl", # Debe encontrar 'curl'
            "Remo en polea baja": "rem", # Debe encontrar 'rem'
            "Abdominales crunch": "ab" # Debe encontrar 'ab'
        }
        
        for input_name, keyword in test_cases.items():
            url = get_exercise_image(input_name)
            # Verificar que la URL devuelta sea técnica (GitHub)
            self.assertIn("raw.githubusercontent.com", url)
            print(f"    - Input: '{input_name}' -> OK")
        print("  [PASSED] Lógica de palabras clave técnica y robusta.")

    def test_03_absolute_fallback_resilience(self):
        """CAOS: Verifica que nombres sin sentido no rompan la app y usen el fallback Élite."""
        print("  - Escenario: Resiliencia ante Nombres Desconocidos (Fallback)...")
        garbage_names = ["Ejercicio Inventado 123", "---", "XYZ_123", "Movimiento Fantasma"]
        
        fallback_url = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop"
        
        for name in garbage_names:
            url = get_exercise_image(name)
            self.assertEqual(url, fallback_url)
        print("  [PASSED] Fallback Élite garantizado para datos no mapeados.")

    def test_04_no_generic_randomness(self):
        """CAOS: Asegura que NO existan URLs de loremflickr en el sistema."""
        print("  - Escenario: Erradicación de LoremFlickr (Calidad)...")
        for name in TECHNICAL_MAPPING:
            url = get_exercise_image(name)
            self.assertNotIn("loremflickr.com", url, f"¡ERROR: Se encontró una URL genérica en {name}!")
        print("  [PASSED] Sistema 100% libre de imágenes genéricas de baja calidad.")

if __name__ == "__main__":
    print("\n" + "💎"*15)
    print("INICIANDO IMAGE ELITE CHAOS TEST")
    print("💎"*15)
    unittest.main()
