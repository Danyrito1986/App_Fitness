import unittest
from models import User, Exercise
from services.calculator import calculate_macros
from datetime import datetime

class TestFitnessLogic(unittest.TestCase):

    def setUp(self):
        # Usuario de prueba: Hombre, 80kg, 180cm, Novato, Aumento de masa
        self.test_user = User(
            id=1,
            nombre="Tester",
            objetivo="Aumento de masa muscular",
            peso_actual=80.0,
            genero="Hombre",
            altura=180.0,
            cuello=40.0,
            cintura=85.0,
            edad=30
        )

    def test_macro_calculations(self):
        """Verifica que los cálculos de macros no fallen y den valores razonables."""
        macros = calculate_macros(self.test_user)
        
        # Verificar claves presentes
        self.assertIn("cal", macros)
        self.assertIn("bf", macros)
        self.assertIn("masa_magra", macros)
        
        # Verificar valores lógicos
        self.assertTrue(macros["cal"] > 1500, "Las calorías deberían ser mayores a 1500")
        self.assertTrue(macros["bf"] > 0, "El % de grasa debe ser positivo")
        self.assertTrue(macros["masa_magra"] < 80, "La masa magra debe ser menor al peso total")
        
        print(f"DEBUG TEST: Macros calculados -> {macros}")

    def test_cardio_logic(self):
        """Simula la lógica de sugerencia de cardio."""
        def get_cardio_suggestion(objetivo):
            if objetivo == "Aumento de masa muscular":
                return "Baja intensidad"
            elif objetivo == "Definición / Quema de Grasa":
                return "LISS moderado"
            return "HIIT"

        self.assertEqual(get_cardio_suggestion(self.test_user.objetivo), "Baja intensidad")
        self.assertEqual(get_cardio_suggestion("Definición / Quema de Grasa"), "LISS moderado")

    def test_storage_key_generation(self):
        """Prueba que la generación de llaves para persistencia sea consistente."""
        mes, dia, ex_id = 1, 1, 99
        key = f"{mes}_{dia}_{ex_id}"
        self.assertEqual(key, "1_1_99")

    def test_exercise_model(self):
        """Verifica el modelo de ejercicio."""
        ex = Exercise(id=1, nombre="Press", series=4, reps=10, rutina_id=1, descanso=60)
        self.assertEqual(ex.descanso, 60)

if __name__ == "__main__":
    print("--- INICIANDO TEST DE PRUEBA Y ERRORES (App_Fitness) ---")
    unittest.main()
