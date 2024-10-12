import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSpacerItem,
    QSizePolicy
)
from PySide6.QtCore import Qt

class FileExplorer(QWidget):
    
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 400, 250)

        # Create a vertical box layout
        self.layout = QVBoxLayout()

        # Create a button for opening the file dialog
        self.open_button = QPushButton("Open File Explorer")
        # Connect the button click event to the file dialog function
        self.open_button.clicked.connect(self.open_file_dialog)

        # Set the style for the button
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

        # Add the button to the layout
        self.layout.addWidget(self.open_button)

        # Create a label to display the selected file path
        self.file_path_label = QLabel("Ruta del archivo: ")
        
        # Set the style for the label
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
        
        # Set minimum size policy for the label to prevent it from expanding too much
        self.file_path_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        # Add the label to the layout
        self.layout.addWidget(self.file_path_label)

        # Add a spacer item to take up the remaining vertical space
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout for the main widget
        self.setLayout(self.layout)

    def open_file_dialog(self):
        # Open a file dialog for selecting a file
        options = QFileDialog.Options()
        # Define allowed file extensions
        allowed_extensions = "Archivos compatibles (*.csv *.xlsx *.xls *.sqlite *.db)"
        # Get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione el archivo: ", "", allowed_extensions, options=options)
        # If a file is selected, update the label with the file path
        if file_path:
            self.file_path_label.setText(f"Ruta del archivo seleccionado: {file_path}")

if __name__ == "__main__":
    # Create the application and the main window
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()  # Show the file explorer window
    sys.exit(app.exec())  # Execute the application