import unittest
import pandas as pd
from src.data_management import Model, UnexpectedError
import numpy as np


class TestLinearRegressionModel(unittest.TestCase):

    def setUp(self):
        """Set up a basic dataset and initialize the model."""
        self.data = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 6, 8, 10]
        })
        self.model = Model()

    def test_initial_attributes(self):
        """Test initial values of model attributes."""
        self.assertIsNone(self.model.formula)
        self.assertIsNone(self.model.r2)
        self.assertIsNone(self.model.mse)
        self.assertIsNone(self.model.pred_line)
        self.assertIsNone(self.model.y_name)
        self.assertIsNone(self.model.x_name)
        self.assertIsNone(self.model.slope)
        self.assertIsNone(self.model.intercept)
        self.assertIsNone(self.model.description)
        self.assertIsNone(self.model.independent_value)
        self.assertIsNone(self.model.target_value)

    def test_create_from_data(self):
        """Test model creation from a dataset."""
        self.model.create_from_data(self.data, 'x', 'y')
        self.assertEqual(self.model.x_name, 'x')
        self.assertEqual(self.model.y_name, 'y')
        self.assertEqual(self.model.slope, 2)
        self.assertEqual(self.model.intercept, 0)
        self.assertAlmostEqual(self.model.r2, 1.0, places=5)
        self.assertAlmostEqual(self.model.mse, 0.0, places=5)
        self.assertEqual(
            self.model.formula,
            'y = 2.00 * x + 0.00'
        )
        self.assertTrue((self.model.pred_line == self.data['y']).all())

    def test_attribute_modification(self):
        """Test direct modification of attributes via setters."""
        self.model.r2 = 0.9
        self.model.mse = 10.5
        self.model.description = "Test description"
        self.assertEqual(self.model.r2, 0.9)
        self.assertEqual(self.model.mse, 10.5)
        self.assertEqual(self.model.description, "Test description")

    def test_invalid_column_names(self):
        """Test handling of invalid column names."""
        # Primero creamos un modelo válido
        self.model.create_from_data(self.data, 'x', 'y')

        # Guardamos los valores anteriores
        previous_values = {attr: getattr(self.model, attr)
                           for attr in vars(self.model)}

        # Probamos con columna x inválida
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(self.data, 'invalid_x', 'y')

        # Verificar que se mantienen los valores anteriores
        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")

        # Probamos con columna y inválida
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(self.data, 'x', 'invalid_y')

        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")

    def test_empty_data(self):
        """Test behavior with empty dataset."""
        # Primero creamos un modelo válido
        self.model.create_from_data(self.data, 'x', 'y')

        # Guardamos los valores anteriores
        previous_values = {attr: getattr(self.model, attr)
                           for attr in vars(self.model)}

        empty_data = pd.DataFrame({'x': [], 'y': []})
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(empty_data, 'x', 'y')

        # Verificar que se mantienen los valores anteriores
        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")

    def test_unaligned_column_sizes(self):
        """Test behavior with misaligned column sizes."""
        # Primero creamos un modelo válido
        self.model.create_from_data(self.data, 'x', 'y')

        # Guardamos los valores anteriores
        previous_values = {attr: getattr(self.model, attr)
                           for attr in vars(self.model)}

        x_series = pd.Series([1, 2], name='x')
        y_series = pd.Series([2, 4, 6], name='y')
        unaligned_data = pd.concat([x_series, y_series], axis=1)
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(unaligned_data, 'x', 'y')

        # Verificar que se mantienen los valores anteriores
        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")

    def test_non_numeric_data(self):
        """Test behavior with non-numeric data."""
        # Primero creamos un modelo válido
        self.model.create_from_data(self.data, 'x', 'y')

        # Guardamos los valores anteriores
        previous_values = {attr: getattr(self.model, attr)
                           for attr in vars(self.model)}

        non_numeric_data = pd.DataFrame({'x': ['a', 'b', 'c'], 'y': [2, 4, 6]})
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(non_numeric_data, 'x', 'y')

        # Verificar que se mantienen los valores anteriores
        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")

    def test_getters_setters(self):
        """Test individual getters and setters."""
        self.model.formula = "y = mx + b"
        self.assertEqual(self.model.formula, "y = mx + b")
        self.model.slope = 2
        self.assertEqual(self.model.slope, 2)
        self.model.intercept = -3
        self.assertEqual(self.model.intercept, -3)

    def test_model_reset_after_new_creation(self):
        """Test that creating a new model after a successful one doesn't retain old values."""
        # Crear primer modelo exitoso
        self.model.create_from_data(self.data, 'x', 'y')
        self.model.description = "New description"

        # Verificar que el primer modelo se creó correctamente y guardar valores
        old_values = {
            'formula': self.model.formula,
            'r2': self.model.r2,
            'mse': self.model.mse,
            'pred_line': self.model.pred_line,
            'y_name': self.model.y_name,
            'x_name': self.model.x_name,
            'slope': self.model.slope,
            'intercept': self.model.intercept,
            'description': self.model.description,
            'independent_value': self.model.independent_value,
            'target_value': self.model.target_value
        }

        # Crear un nuevo modelo con datos diferentes
        new_data = pd.DataFrame({
            'a': [10, 20, 30, 38],
            'b': [1, 2, 3, 4]
        })
        self.model.create_from_data(new_data, 'a', 'b')

        # Verificar que todos los valores son diferentes
        current_values = {
            'formula': self.model.formula,
            'r2': self.model.r2,
            'mse': self.model.mse,
            'pred_line': self.model.pred_line,
            'y_name': self.model.y_name,
            'x_name': self.model.x_name,
            'slope': self.model.slope,
            'intercept': self.model.intercept,
            'description': self.model.description,
            'independent_value': self.model.independent_value,
            'target_value': self.model.target_value
        }

        for attr in old_values:
            if attr == 'pred_line' or attr == 'independent_value' or attr == 'target_value':
                # Para pred_line, verificamos que los arrays son diferentes
                self.assertFalse((len(old_values[attr]) == len(current_values[attr])),
                                 f"{attr} el array de valores esperados no deberian tener la misma longitud")
            else:
                self.assertNotEqual(old_values[attr], current_values[attr],
                                    f"{attr} no debería mantener el valor anterior")

    def test_model_clean_after_error(self):
        """Test that creating a new model after a corrupted attempt maintains previous values."""
        # Crear primer modelo exitoso
        self.model.create_from_data(self.data, 'x', 'y')

        # Guardar valores anteriores
        previous_values = {attr: getattr(self.model, attr)
                           for attr in vars(self.model)}

        # Intentar crear con datos no alineados
        x_series = pd.Series([1, 2], name='x')
        y_series = pd.Series([2, 4, 6], name='y')
        unaligned_data = pd.concat([x_series, y_series], axis=1)

        # Crear primer modelo exitoso
        with self.assertRaises(UnexpectedError):
            self.model.create_from_data(unaligned_data, 'x', 'y')

        # Verificar que se mantienen los valores anteriores
        # Verificar que se mantienen los valores anteriores
        for attr in vars(self.model):
            current_value = getattr(self.model, attr)
            previous_value = previous_values[attr]

            if isinstance(current_value, (pd.Series, pd.DataFrame, np.ndarray)):
                pd.testing.assert_series_equal(current_value, previous_value) if isinstance(current_value, pd.Series) else \
                    np.testing.assert_array_equal(
                        current_value, previous_value)
            else:
                self.assertEqual(current_value, previous_value,
                                 f"El atributo {attr} debería mantener su valor anterior")


if __name__ == "__main__":
    unittest.main()
