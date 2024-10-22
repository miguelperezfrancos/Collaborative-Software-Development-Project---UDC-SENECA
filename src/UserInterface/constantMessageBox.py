from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class InputDialog(QDialog):

    """
    This class creates a dialog interface that allows user to 
    introduce a constant to fill nan values on the selcted columns.
    """

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Introduce a value")
        
        # Create layout
        layout = QVBoxLayout()

        self.label = QLabel("Choose a value:")
        layout.addWidget(self.label)

        # create text input box
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)
        
        # create buttons
        self.back_button = QPushButton("Back", self)
        self.enter_button = QPushButton("Enter", self)
        layout.addWidget(self.back_button)
        layout.addWidget(self.enter_button)
        
        # Add events to the buttons
        self.back_button.clicked.connect(self.go_back)
        self.enter_button.clicked.connect(self.enter_value)
        
        self.setLayout(layout)

    def go_back(self):
        """
        This function is the event for pressing back button.
        It will close the dialog
        """
        self.reject() 

    def enter_value(self):
        """
        This function is the event for pressing eneter button.
        It will store the entered value and then closed with
        sccepted result.
        """
        self.entered_value = self.input_field.text()
        self.accept()  