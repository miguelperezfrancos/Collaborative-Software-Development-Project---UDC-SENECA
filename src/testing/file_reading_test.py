import unittest
import pandas as pd
import sqlite3
import os
from pathlib import Path
from data_management.fileReader import FileReader, ParseError

class TestFileReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Crear archivos de prueba necesarios"""
        cls.base_path = Path("/Users/rafa/Documents/Uni/Cuatri3/software_engineering/sample_data")
        
        # Datos de prueba consistentes
        cls.test_data = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4.5, 5.5, 6.5],
            'C': ['x', 'y', 'z']
        })
        
        # Crear CSV válido
        cls.csv_path = cls.base_path / "test_data.csv"
        cls.test_data.to_csv(cls.csv_path, index=False)
        
        # Crear Excel válido
        cls.excel_path = cls.base_path / "test_data.xlsx"
        cls.test_data.to_excel(cls.excel_path, index=False)
        
        # Crear SQLite válido
        cls.db_path = cls.base_path / "test_data.db"
        conn = sqlite3.connect(cls.db_path)
        cls.test_data.to_sql('test_table', conn, index=False)
        conn.close()
        
        # Path al archivo corrupto
        cls.corrupted_path = Path("/Users/rafa/Documents/Uni/Cuatri3/software_engineering/sample_data/corrupted_file.csv")

    def setUp(self):
        """Inicializar FileReader para cada test"""
        self.reader = FileReader()

    def test_valid_csv(self):
        """Test lectura de CSV válido"""
        df = self.reader.parse_file(str(self.csv_path))
        self.assertIsInstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, self.test_data)

    def test_valid_excel(self):
        """Test lectura de Excel válido"""
        df = self.reader.parse_file(str(self.excel_path))
        self.assertIsInstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, self.test_data)

    def test_valid_sqlite(self):
        """Test lectura de SQLite válido"""
        df = self.reader.parse_file(str(self.db_path))
        self.assertIsInstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, self.test_data)

    def test_corrupted_file(self):
        """Test manejo de archivo corrupto"""
        with self.assertRaises(ParseError):
            self.reader.parse_file(str(self.corrupted_path))

    def test_nonexistent_file(self):
        """Test manejo de archivo inexistente"""
        with self.assertRaises(ParseError):
            self.reader.parse_file("nonexistent.csv")

    def test_unsupported_format(self):
        """Test manejo de formato no soportado"""
        with self.assertRaises(ParseError):
            self.reader.parse_file("file.txt")

    @classmethod
    def tearDownClass(cls):
        """Limpiar archivos de prueba creados"""
        try:
            os.remove(cls.csv_path)
            os.remove(cls.excel_path)
            os.remove(cls.db_path)
        except Exception as e:
            print(f"Error limpiando archivos: {e}")

if __name__ == '__main__':
    unittest.main()