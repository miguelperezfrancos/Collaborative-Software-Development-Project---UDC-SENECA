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

        # Add the button to the layout
        self.layout.addWidget(self.open_button)

        # Create a label to display the selected file path
        self.file_path_label = QLabel("Selected file path: ")
        
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
        allowed_extensions = "Archivos permitidos (*.csv *.xlsx *.xls *.sqlite *.db)"
        # Get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecciona el archivo deseado: ", "", allowed_extensions, options=options)
        # If a file is selected, update the label with the file path
        if file_path:
            self.file_path_label.setText(f"Ruta del archivo seleccionado: {file_path}")

if __name__ == "__main__":
    # Create the application and the main window
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()  # Show the file explorer window
    sys.exit(app.exec())  # Execute the application

