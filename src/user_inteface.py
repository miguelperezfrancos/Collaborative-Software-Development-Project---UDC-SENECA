import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt
from file_reader import FileReader
import pandas as pd  

class FileExplorer(QWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.open_button = QPushButton("Open File Explorer")
        self.open_button.clicked.connect(self.open_file_dialog)

        self.open_button.setStyleSheet(""" 
            QPushButton {
                background-color: #007BFF;  
                color: white;                
                font-size: 18px;            
                font-weight: bold;          
                border: none;               
                border-radius: 20px;        
                padding: 12px 30px;         
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);  
                transition: background-color 0.3s ease;   
            }
            QPushButton:hover {
                background-color: #0056b3;  
            }
            QPushButton:pressed {
                background-color: #003d80;   
                box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5); 
            }
        """)

        self.layout.addWidget(self.open_button)
        self.file_path_label = QLabel("Ruta del archivo: ")
        
        self.file_path_label.setStyleSheet(""" 
            QLabel {
                background-color: #FFFDD0;  
                color: #333;                
                font-size: 14px;           
                font-weight: bold;         
                border: 1px solid #d1d1d1; 
                border-radius: 7px;      
                padding: 8px;             
                margin-top: 5px;          
            }
        """)
        
        self.file_path_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.layout.addWidget(self.file_path_label)
        
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        allowed_extensions = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccione el archivo: ", "", allowed_extensions, options=options)
        
        if file_path:
            self.file_path_label.setText(f"Ruta del archivo seleccionado: {file_path}")
            self.load_file(file_path)

    def load_file(self, file_path):
        reader = FileReader()
        try:
            df = reader.parse_file(file_path)

            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            # Verificar si el DataFrame está vacío
            if df is None or (df.shape[0] == 0 and df.shape[1] == 0):
                raise ValueError("File Not Containing Data.")

            if df.shape[0] > 0 and df.shape[1] > 0:
                self.table_widget.setRowCount(df.shape[0])
                self.table_widget.setColumnCount(df.shape[1])
                self.table_widget.setHorizontalHeaderLabels(df.columns)

                for i in range(df.shape[0]):
                    for j in range(df.shape[1]):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
            else:
                raise ValueError("Reading Error.")

        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            self.show_error_message("Error Processing the File: " + str(e))
        except Exception as e:
            self.show_error_message("Unknown Error")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec())
