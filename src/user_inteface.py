import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt
from file_reader import FileReader
import pandas as pd

class FileExplorer(QWidget):
    
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        # Main vertical layout
        self.layout = QVBoxLayout()

        # Horizontal layout for file path label and open button
        self.h_layout = QHBoxLayout()

        # Label to display selected file path
        self.file_path_label = QLabel("File_path: ")
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
        self.file_path_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.file_path_label2 = QLabel("")
        self.file_path_label2.setStyleSheet(""" 
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
        self.file_path_label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  

        # Button to open file explorer dialog
        self.open_button = QPushButton("Open File Explorer")
        self.open_button.clicked.connect(self.open_file_dialog)  # Connect button click to open dialog
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

        # Add label and button to the horizontal layout
        self.h_layout.addWidget(self.file_path_label)
        self.h_layout.addWidget(self.file_path_label2)
        self.h_layout.addWidget(self.open_button)

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(self.h_layout)

        # Table to display file content
        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to expanding
        self.layout.addWidget(self.table_widget)

        # Horizontal layout for combo boxes
        self.h2_layout = QHBoxLayout()

        # Combo box 1 for selecting a column
        self.combo_box1 = QComboBox()
        self.combo_box1.setStyleSheet(""" 
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.combo_box1.addItem("Select a column")  # Default item
        self.h2_layout.addWidget(self.combo_box1)

        # Combo box 2 for selecting a column
        self.combo_box2 = QComboBox()
        self.combo_box2.setStyleSheet(""" 
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.combo_box2.addItem("Select a column")  # Default item
        self.h2_layout.addWidget(self.combo_box2)

        # Add combo box layout to the main layout
        self.layout.addLayout(self.h2_layout)

        # Set main layout
        self.setLayout(self.layout)

        # Set stretch for the table to expand
        self.layout.setStretch(1, 10)  # 10: the table has more space to expand
        self.layout.setStretch(2, 1)  # 1: the combo box layout takes less space


    def open_file_dialog(self):
        # File dialog settings
        options = QFileDialog.Options()
        allowed_extensions = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccione el archivo: ", "", allowed_extensions, options=options)
        
        # If a file is selected, load it into the table
        if file_path:
            self.file_path_label2.setText(f"{file_path}")
            self.load_file(file_path)

    def load_file(self, file_path):
        reader = FileReader()
        try:
            df = reader.parse_file(file_path)

            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            # If DataFrame has content, populate the table and combo boxes
            if df.shape[0] > 0 and df.shape[1] > 0:
                self.table_widget.setRowCount(df.shape[0])
                self.table_widget.setColumnCount(df.shape[1])
                self.table_widget.setHorizontalHeaderLabels(df.columns)

                # Fill the table with the DataFrame content
                for i in range(df.shape[0]):
                    for j in range(df.shape[1]):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

                # Populate combo boxes with column names
                self.combo_box1.clear()
                self.combo_box1.addItem("Select a column")
                self.combo_box1.addItems(df.columns)

                self.combo_box2.clear()
                self.combo_box2.addItem("Select a column")
                self.combo_box2.addItems(df.columns)
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
    
    # Create and show the FileExplorer widget
    explorer = FileExplorer()
    explorer.show()
    
    # Start the application's event loop
    sys.exit(app.exec())
