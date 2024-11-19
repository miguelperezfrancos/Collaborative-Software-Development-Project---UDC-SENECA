from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
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
        self._x_input = helper.create_text_box(enabled=True)
        self._result_label = QLabel()
        self._predict_button = helper.create_button(text='predict', event=self._predict)

        

        button_layout = QHBoxLayout()
        button_layout.addWidget(self._predict_button)
        button_layout.setAlignment(Qt.AlignRight)

        input_ly = QGridLayout()
        input_ly.addWidget(self._x_label, 0, 0)
        input_ly.addWidget(self._x_input, 0, 1)
        input_ly.addWidget(self._result_label, 1, 0, 1, 1)
        
        helper.set_layout(layout=layout, items=[
            input_ly,
            button_layout
        ])

        layout.setAlignment(Qt.AlignCenter)
        
        self.setVisible(False)
  

    @Slot(Model)
    def update_model(self, model: Model):
        self._model = model
        text = f"{self._model.x_name}"
        self._x_label.setText(text)
        self._x_input.setText('')

    def _predict(self):

        input_value = self._x_input.text()
        
        try:
            rpred = self._model.slope * float(input_value) + self._model.intercept
            self._result_label.setText(f'{self._model.y_name}: {rpred}')
        except:
            helper.show_error_message('ERROR: you must enter a valid number')