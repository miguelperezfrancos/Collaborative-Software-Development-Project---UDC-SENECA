from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)
import sys
import os 
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)

from PySide6.QtCore import Slot
import UserInterface.UIHelpers as helper
from src.dataManagement import Model


"""
This module contins the widget that will allow the user to make predictions
with a created or loaded model.
"""

class Predict(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()
        self._model = None
        self._x_label = QLabel()
        self._x_input = helper.create_text_box()
        self._x_input.setEnabled(True)
        self._result = QLabel()
        self._predict_button = helper.create_button(text='predict', event=self._predict)

        helper.set_layout(layout=layout, items=[
            self._x_label,
            self._x_input,
            self._result,
            self._predict_button
        ])

        self.setVisible(False)
        self.setLayout(layout)

    @Slot(Model)
    def update_model(self, model: Model):
        self._model = model
        self._x_label.setText(self._model.x_name)

    def _predict(self):

        input_value = self._x_input.text()
        
        try:
            rpred = self._model.slope * float(input_value) + self._model.intercept
            self._result.setText(f'Prediction result: {rpred}')
        except:
            helper.show_error_message('ERROR: you must enter a valid number')