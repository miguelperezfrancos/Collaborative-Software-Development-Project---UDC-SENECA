"""Module for making predictions with created or loaded models.

This module contains the widget that allows users to make predictions
with a created or loaded model.
"""

import os
import sys
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot, Qt

# Add repository root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)

import user_interface.ui_helpers as helper
from src.data_management import Model


class Predict(QWidget):
    """Widget for making predictions using a model."""

    def __init__(self):
        """Initialize the prediction widget."""
        super().__init__()

        # Create main container widget
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Main layout for the container
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        main_layout.addWidget(self.container)

        # Internal layout for components
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(layout)

        # Initialize instance variables
        self._model = None
        self._x_label = QLabel()
        self._x_input = helper.create_text_box(enabled=True)
        self._result_label = QLabel()
        self._predict_button = helper.create_button(
            text='predict',
            event=self._predict
        )

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self._predict_button)
        button_layout.setAlignment(Qt.AlignRight)

        # Create input layout
        input_layout = QGridLayout()
        input_layout.addWidget(self._x_label, 0, 0)
        input_layout.addWidget(self._x_input, 0, 1)
        input_layout.addWidget(self._result_label, 1, 0, 1, 1)
        
        # Set main layout components
        helper.set_layout(
            layout=layout,
            items=[input_layout, button_layout]
        )

        layout.setAlignment(Qt.AlignCenter)
        self.setVisible(False)

    @Slot(Model)
    def update_model(self, model: Model):
        """Update the model used for predictions.

        Args:
            model (Model): New model to use for predictions.
        """
        self._model = model
        text = f"{self._model.x_name}"
        self._x_label.setText(text)
        self._x_input.setText('')
        self._result_label.setText('')

    def _predict(self):
        """Make a prediction using the current model and input value."""
        input_value = self._x_input.text()
        
        try:
            prediction = (self._model.slope * float(input_value) +
                         self._model.intercept)
            self._result_label.setText(
                f'{self._model.y_name}: {prediction}'
            )
        except ValueError:
            helper.show_error_message('ERROR: you must enter a valid number')