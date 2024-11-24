import unittest
import pandas as pd
from src.data_management import Model


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
        with self.assertRaises(KeyError):
            self.model.create_from_data(self.data, 'invalid_x', 'y')
        with self.assertRaises(KeyError):
            self.model.create_from_data(self.data, 'x', 'invalid_y')

    def test_empty_data(self):
        """Test behavior with empty dataset."""
        empty_data = pd.DataFrame({'x': [], 'y': []})
        with self.assertRaises(ValueError):
            self.model.create_from_data(empty_data, 'x', 'y')

    def test_unaligned_column_sizes(self):
        """Test behavior with misaligned column sizes."""
        unaligned_data = pd.DataFrame({'x': [1, 2], 'y': [2, 4, 6]})
        with self.assertRaises(ValueError):
            self.model.create_from_data(unaligned_data, 'x', 'y')

    def test_non_numeric_data(self):
        """Test behavior with non-numeric data."""
        non_numeric_data = pd.DataFrame({'x': ['a', 'b', 'c'], 'y': [2, 4, 6]})
        with self.assertRaises(ValueError):
            self.model.create_from_data(non_numeric_data, 'x', 'y')

    def test_getters_setters(self):
        """Test individual getters and setters."""
        self.model.formula = "y = mx + b"
        self.assertEqual(self.model.formula, "y = mx + b")
        self.model.slope = 2
        self.assertEqual(self.model.slope, 2)
        self.model.intercept = -3
        self.assertEqual(self.model.intercept, -3)


if __name__ == "__main__":
    unittest.main()
