import unittest
import pandas as pd
import numpy as np
from data_management.dataManager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear DataFrame de prueba con valores nulos
        self.test_data = pd.DataFrame({
            'col1': [1, 2, np.nan, 4, 5],
            'col2': [10, np.nan, 30, 40, 50],
            'col3': ['a', 'b', 'c', 'd', 'e']
        })
        self.data_manager = DataManager(self.test_data)

    def test_data_initialization(self):
        """Test de inicialización y getter/setter de datos"""
        # Test getter
        self.assertTrue(isinstance(self.data_manager.data, pd.DataFrame))
        self.assertEqual(len(self.data_manager.data), 5)
        
        # Test setter con DataFrame válido
        new_df = pd.DataFrame({'test': [1, 2, 3]})
        self.data_manager.data = new_df
        self.assertEqual(len(self.data_manager.data), 3)
        
        # Test setter con tipo inválido
        with self.assertRaises(ValueError):
            self.data_manager.data = [1, 2, 3]

    def test_get_columns(self):
        """Test obtención de nombres de columnas por índice"""
        self.data_manager.data = self.test_data
        self.assertEqual(self.data_manager.get_columns(0), 'col1')
        self.assertEqual(self.data_manager.get_columns(1), 'col2')
        self.assertEqual(self.data_manager.get_columns(2), 'col3')

    def test_detect_nan(self):
        """Test detección de valores nulos"""
        self.data_manager.data = self.test_data
        self.assertEqual(self.data_manager.detect('col1'), 1)  # Una fila con NaN
        self.assertEqual(self.data_manager.detect('col2'), 1)  # Una fila con NaN
        self.assertEqual(self.data_manager.detect('col3'), 0)  # Sin NaN

    def test_delete_nan(self):
        """Test eliminación de filas con valores nulos"""
        self.data_manager.data = self.test_data
        
        # Eliminar NaN de una columna
        self.data_manager.delete(['col1'])
        self.assertEqual(len(self.data_manager.data), 4)
        
        # Resetear datos
        self.data_manager.data = self.test_data
        
        # Eliminar NaN de múltiples columnas
        self.data_manager.delete(['col1', 'col2'])
        self.assertEqual(len(self.data_manager.data), 3)
        self.assertTrue(self.data_manager.data['col1'].notna().all())
        self.assertTrue(self.data_manager.data['col2'].notna().all())

    def test_replace_nan_mean(self):
        """Test reemplazo de NaN con media"""
        self.data_manager.data = self.test_data
        self.data_manager.replace(['col1', 'col2'], 'mean')
        
        # Verificar que no hay NaN
        self.assertEqual(self.data_manager.detect('col1'), 0)
        self.assertEqual(self.data_manager.detect('col2'), 0)
        
        # Verificar que los valores son correctos
        expected_mean_col1 = self.test_data['col1'].mean()
        expected_mean_col2 = self.test_data['col2'].mean()
        
        self.assertTrue(any(self.data_manager.data['col1'] == expected_mean_col1))
        self.assertTrue(any(self.data_manager.data['col2'] == expected_mean_col2))

    def test_replace_nan_median(self):
        """Test reemplazo de NaN con mediana"""
        self.data_manager.data = self.test_data
        self.data_manager.replace(['col1', 'col2'], 'median')
        
        # Verificar que no hay NaN
        self.assertEqual(self.data_manager.detect('col1'), 0)
        self.assertEqual(self.data_manager.detect('col2'), 0)
        
        # Verificar que los valores son correctos
        expected_median_col1 = self.test_data['col1'].median()
        expected_median_col2 = self.test_data['col2'].median()
        
        self.assertTrue(any(self.data_manager.data['col1'] == expected_median_col1))
        self.assertTrue(any(self.data_manager.data['col2'] == expected_median_col2))

    def test_replace_nan_constant(self):
        """Test reemplazo de NaN con valor constante"""
        self.data_manager.data = self.test_data
        constant_value = 999
        self.data_manager.replace(['col1', 'col2'], constant_value)
        
        # Verificar que no hay NaN
        self.assertEqual(self.data_manager.detect('col1'), 0)
        self.assertEqual(self.data_manager.detect('col2'), 0)
        
        # Verificar que los valores fueron reemplazados por la constante
        nan_mask_col1 = self.test_data['col1'].isna()
        nan_mask_col2 = self.test_data['col2'].isna()
        
        self.assertTrue(all(self.data_manager.data.loc[nan_mask_col1, 'col1'] == constant_value))
        self.assertTrue(all(self.data_manager.data.loc[nan_mask_col2, 'col2'] == constant_value))

    def test_replace_invalid_value(self):
        """Test reemplazo con valor inválido"""
        self.data_manager.data = self.test_data
        # Intentar reemplazar con un string que no sea 'mean' o 'median'
        self.data_manager.replace(['col1'], 'invalid_value')
        # Verificar que los datos no cambiaron
        self.assertEqual(self.data_manager.detect('col1'), 1)

    def test_replace_non_numeric_column(self):
        """Test reemplazo en columna no numérica"""
        self.data_manager.data = self.test_data
        original_values = self.test_data['col3'].copy()
        
        # Intentar reemplazar en una columna de strings
        self.data_manager.replace(['col3'], 'mean')
        
        # Verificar que la columna no cambió
        pd.testing.assert_series_equal(self.data_manager.data['col3'], original_values)

if __name__ == '__main__':
    unittest.main()
