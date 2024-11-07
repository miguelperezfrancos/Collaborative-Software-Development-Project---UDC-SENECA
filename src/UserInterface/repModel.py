from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt
import UserInterface.UIHelpers as helper
from src.dataManagement import Model

"""
This module cretes the widget that shows up when you load an
existing model.
"""

class RepModel(QWidget):

    def __init__(self):
        super().__init__()

        #model that is working with
        self._model = Model()

         # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add title label
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Create a sub-layout for indented content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 0, 0, 0)  # Add left indent

        # Add formula label
        self.formula_label = QLabel()
        self.formula_label.setAlignment(Qt.AlignLeft)
        self.formula_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(self.formula_label)

        # Add R² label
        self.r2_label = QLabel()
        self.r2_label.setAlignment(Qt.AlignLeft)
        self.r2_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(self.r2_label)

        # Add MSE label
        self.mse_label = QLabel()
        self.mse_label.setAlignment(Qt.AlignLeft)
        self.mse_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(self.mse_label)

        # Add description label
        self.description_label = QLabel()
        self.description_label.setAlignment(Qt.AlignLeft)
        self.description_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(self.description_label)

        # Add the sub-layout to the main layout
        layout.addLayout(content_layout)

    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = value

    def update_model(self):
        self.formula_label.setText(f'Formula: {self._model.formula}')
        self.r2_label.setText(f'R2: {self._model.r2:.4f}')
        self.mse_label.setText(f'MSE: {self._model.mse:.4f}')
        self.description_label.setText(f'Description: {self._model.description}')