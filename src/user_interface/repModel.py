"""Module for displaying model information, formula, metrics and description."""

# Standard library imports
import os
import sys

# Third-party imports
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

# Add repository root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)

# Local imports
import user_interface.ui_helpers as helper
from src.data_management import Model, save_model


class RepModel(QWidget):
    """Widget for displaying and managing regression model information."""

    def __init__(self):
        """Initialize the model representation widget."""
        super().__init__()

        # Create main container widget
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Internal layout for components
        internal_layout = QVBoxLayout()
        internal_layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(internal_layout)
        
        # Initialize model
        self._model = Model()
        
        # Create UI components
        self.description_input = helper.create_description_box()
        self.description_input.setPlaceholderText(
            "Enter a description for the model..."
        )
        
        self.save_button = helper.create_button(
            text="Save Model",
            event=self._save_model
        )
        
        self._model_info = QLabel()

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.setAlignment(Qt.AlignRight)

        # Add widgets to internal layout
        internal_layout.addWidget(self._model_info)
        internal_layout.addWidget(self.description_input)
        internal_layout.addLayout(button_layout)
        
        # Center align everything
        internal_layout.setAlignment(Qt.AlignCenter)

    @Slot(Model)
    def _update_model(self, model: Model):
        """Update the current working model.

        Args:
            model: New model instance to display.
        """
        self._model = model
        self._get_graph_data()

    def _get_graph_data(self):
        """Update displayed model information and adjust widget layout."""
        text = (
            f"<b style='font-size: 16pt; color: #c2ffff'>{self._model.formula}"
            f"</b><br>"
            f"<font size='6' color='#16A085'>R²: {self._model.r2:.3f}    "
            f"</font>"
            f"<font size='6' color='#E74C3C'>MSE: {self._model.mse:.3f}"
            f"</font><br>"
        )
    
        if self._model.description is not None:
            text += (f"<font size='6' color='#E74C3C'>"
                    f"{self._model.description}</font>")
            self.description_input.setVisible(False)
            self.save_button.setVisible(False)
        else:
            self.description_input.setText('')
            self.description_input.setVisible(True)
            self.save_button.setVisible(True)

        self._model_info.setText(text)
        font = QFont("Arial", 12, QFont.Bold)
        self._model_info.setFont(font)

    def _save_model(self):
        """Handle model saving functionality."""
        if not self._model:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Model",
            "",
            "Joblib Files (*.joblib)"
        )
        
        if not file_path:
            return

        try:
            save_model(
                file_path=file_path,
                formula=self._model.formula,
                input=self._model.x_name,
                output=self._model.y_name,
                r2=self._model.r2,
                mse=self._model.mse,
                description=self.description_input.toPlainText(),
                slope=self._model.slope,
                intercept=self._model.intercept
            )
            QMessageBox.information(
                self,
                "Saving Model",
                "Model successfully saved"
            )
        except Exception as e:
            QMessageBox.information(
                self,
                "Saving model",
                f"Unexpected error occurred: {e}"
            )