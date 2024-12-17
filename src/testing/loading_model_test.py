import unittest
import os
from data_management.modelFileManager import save_model, load_model
from data_management import Model


class TestModelFileManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/Users/rafa/Documents/Uni/Cuatri3/software_engineering/sample_data"
        self.test_file = os.path.join(self.test_dir, "test_model.joblib")
        self.corrupted_file = os.path.join(
            self.test_dir, "corrupted_model.joblib")

    def tearDown(self):
        # Limpiamos archivos de prueba después de cada test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_valid_model(self):
        """Test guardar y cargar un modelo válido"""
        save_model(
            self.test_file,
            formula="2x + 1",
            input="x",
            output="y",
            r2=0.95,
            mse=0.02,
            description="Modelo de prueba",
            slope=2.0,
            intercept=1.0
        )

        modelo_cargado = load_model(self.test_file)

        self.assertEqual(modelo_cargado.formula, "2x + 1")
        self.assertEqual(modelo_cargado.x_name, "x")
        self.assertEqual(modelo_cargado.y_name, "y")
        self.assertEqual(modelo_cargado.r2, 0.95)
        self.assertEqual(modelo_cargado.mse, 0.02)
        self.assertEqual(modelo_cargado.description, "Modelo de prueba")
        self.assertEqual(modelo_cargado.slope, 2.0)
        self.assertEqual(modelo_cargado.intercept, 1.0)

    def test_save_incomplete_model(self):
        """Test intentar guardar un modelo con parámetros faltantes"""
        with self.assertRaises(Exception):
            save_model(
                self.test_file,
                formula=None,  # Parámetro faltante
                input="x",
                output="y",
                r2=0.95,
                mse=0.02,
                description="Modelo incompleto",
                slope=2.0,
                intercept=1.0
            )

    def test_load_nonexistent_file(self):
        """Test intentar cargar un archivo que no existe"""
        archivo_inexistente = os.path.join(self.test_dir, "no_existe.joblib")
        with self.assertRaises(ValueError):
            load_model(archivo_inexistente)

    def test_load_corrupted_file(self):
        """Test intentar cargar un archivo corrupto"""
        with self.assertRaises(ValueError):
            load_model(self.corrupted_file)

    def test_save_invalid_path(self):
        """Test intentar guardar en una ruta inválida"""
        ruta_invalida = "/ruta/invalida/modelo.joblib"
        with self.assertRaises(Exception):
            save_model(
                ruta_invalida,
                formula="2x + 1",
                input="x",
                output="y",
                r2=0.95,
                mse=0.02,
                description="Modelo de prueba",
                slope=2.0,
                intercept=1.0
            )


if __name__ == '__main__':
    unittest.main()
