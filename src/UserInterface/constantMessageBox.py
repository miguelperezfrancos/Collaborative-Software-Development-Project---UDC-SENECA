from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # Configuración del diálogo
        self.setWindowTitle("Introducir Constante")
        
        # Crear el layout
        layout = QVBoxLayout()

        # Etiqueta para instrucciones
        self.label = QLabel("Introduce una constante para preprocesar los datos:")
        layout.addWidget(self.label)

        # Barra de entrada de texto (QLineEdit)
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)
        
        # Botones: Back y Enter
        self.back_button = QPushButton("Back", self)
        self.enter_button = QPushButton("Enter", self)
        
        # Añadir botones al layout
        layout.addWidget(self.back_button)
        layout.addWidget(self.enter_button)
        
        # Conectar los botones a sus funciones
        self.back_button.clicked.connect(self.go_back)
        self.enter_button.clicked.connect(self.enter_value)
        
        # Configurar el layout del diálogo
        self.setLayout(layout)

    def go_back(self):
        # Acción para el botón "Back"
        self.reject()  # Cierra el diálogo con resultado 'rechazado'

    def enter_value(self):
        # Acción para el botón "Enter"
        self.entered_value = self.input_field.text()
        print(f"Valor introducido: {self.entered_value}")
        self.accept()  # Cierra el diálogo con resultado 'aceptado'