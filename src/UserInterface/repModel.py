from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)

from PySide6.QtCore import Signal, Slot, Qt
import UserInterface.UIHelpers as helper

"""
This module cretes the widget that shows up when you load an
existing model.
"""

class repModel(QWidget):

    def __init__(self):
        super().__init__()

         # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add title label
        title_label = QLabel("Current Model")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Create a sub-layout for indented content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 0, 0, 0)  # Add left indent

        # Add formula label
        formula_label = QLabel("Formula: y = mx + a")
        formula_label.setAlignment(Qt.AlignLeft)
        formula_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(formula_label)

        # Add R² label
        r2_label = QLabel("R²: 0.92")
        r2_label.setAlignment(Qt.AlignLeft)
        r2_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(r2_label)

        # Add MSE label
        mse_label = QLabel("MSE: 0.11")
        mse_label.setAlignment(Qt.AlignLeft)
        mse_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(mse_label)

        # Add description label
        description_label = QLabel("Bla bla bla bla")
        description_label.setAlignment(Qt.AlignLeft)
        description_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(description_label)

        # Add the sub-layout to the main layout
        layout.addLayout(content_layout)