from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)
import sys
import os 
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot, Qt
import UserInterface.UIHelpers as helper
from src.dataManagement import Model


"""
This module contins the widget that will allow the user to make predictions
with a created or loaded model.
"""

class Predict(QWidget):

    def __init__(self):

        super().__init__()

        # Crear widget contenedor principal
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Layout principal que contendrá el container
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        main_layout.addWidget(self.container)

        # Layout interno para los componentes
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(layout)

        self._model = None
        self._x_label = QLabel()
        self._x_input = helper.create_text_box()
        self._x_input.setEnabled(True)
        self._result = QLabel()
        self._predict_button = helper.create_button(text='predict', event=self._predict)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self._predict_button)
        button_layout.setAlignment(Qt.AlignRight)

        input_ly = QHBoxLayout()
        input_ly.addWidget(self._x_label)
        input_ly.addWidget(self._x_input)
        input_ly.setAlignment(Qt.AlignCenter)

        helper.set_layout(layout=layout, items=[
            input_ly,
            self._result,
            button_layout
        ])
        
        self.setVisible(False)
  

    @Slot(Model)
    def update_model(self, model: Model):
        self._model = model
        text = f"<b style='font-size: 16pt; color: #c2ffff'>{self._model.x_name} = </b><br>"
        self._x_label.setText(text)
        font = QFont("Arial", 12, QFont.Bold)  # Cambiar la fuente a Arial, tamaño 12 y en negrita
        self._x_label.setFont(font)

    def _predict(self):

        input_value = self._x_input.text()
        
        try:
            rpred = self._model.slope * float(input_value) + self._model.intercept
            self._result.setText(f'Prediction result: {rpred}')
        except:
            helper.show_error_message('ERROR: you must enter a valid number')