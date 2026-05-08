import unittest
from seed_advanced_local import seed_advanced_exercises

class TestSeedIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generamos los ejercicios en memoria para analizarlos
        cls.ejercicios = seed_advanced_exercises(execute_insert=False)

    def test_total_count(self):
        """Verifica que el número total de ejercicios sea el esperado (2160)."""
        self.assertEqual(len(self.ejercicios), 2160)

    def test_required_fields(self):
        """Verifica que cada ejercicio tenga todos los campos necesarios."""
        required_fields = ["nombre", "series", "reps", "descanso", "genero", "nivel", "objetivo", "mes", "semana", "dia"]
        for ex in self.ejercicios:
            for field in required_fields:
                self.assertIn(field, ex, f"Campo faltante: {field} en {ex.get('nombre')}")

    def test_progression_logic(self):
        """Verifica que la semana 3 tenga menos repeticiones que la semana 1 (progresión de carga)."""
        # Buscamos el mismo ejercicio en S1 y S3
        ex_s1 = [e for e in self.ejercicios if e['semana'] == 1 and e['mes'] == 1 and e['dia'] == 1 and e['genero'] == 'Hombre' and e['objetivo'] == 'Aumento de masa muscular'][0]
        ex_s3 = [e for e in self.ejercicios if e['semana'] == 3 and e['mes'] == 1 and e['dia'] == 1 and e['genero'] == 'Hombre' and e['objetivo'] == 'Aumento de masa muscular'][0]
        
        self.assertLess(ex_s3['reps'], ex_s1['reps'], f"La progresión de reps falló para {ex_s1['nombre']}")

    def test_deload_week(self):
        """Verifica que la semana 4 (descarga) tenga solo 2 series."""
        ex_s4 = [e for e in self.ejercicios if e['semana'] == 4][0]
        self.assertEqual(ex_s4['series'], 2, f"La semana de descarga falló para {ex_s4['nombre']}")

    def test_uniqueness(self):
        """Verifica que no haya duplicados exactos (mismo nombre en mismo día/semana/mes/objetivo/genero)."""
        seen = set()
        for ex in self.ejercicios:
            key = (ex['nombre'], ex['mes'], ex['semana'], ex['dia'], ex['objetivo'], ex['genero'])
            self.assertNotIn(key, seen, f"Duplicado detectado: {ex['nombre']} en M{ex['mes']}S{ex['semana']}D{ex['dia']}")
            seen.add(key)

if __name__ == "__main__":
    unittest.main()
