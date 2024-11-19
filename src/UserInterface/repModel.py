from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFileDialog,
    QMessageBox,
    QHBoxLayout
)
import sys
import os 
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)

from src.dataManagement import Model, save_model
import UserInterface.UIHelpers as helper
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot, Qt
import UserInterface.UIHelpers as helper
from src.dataManagement import Model

"""
This module displays information about the model, its formula,
r2, mean squared error and description.
"""

class RepModel(QWidget):

    def __init__(self):
        super().__init__()

        # Crear un widget contenedor principal
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Crear el layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del layout principal
        self.setLayout(main_layout)
        
        # Agregar el contenedor al layout principal
        main_layout.addWidget(self.container)
        
        # Layout interno para los componentes
        internal_layout = QVBoxLayout()
        internal_layout.setContentsMargins(10, 10, 10, 10)  # Padding interno
        self.container.setLayout(internal_layout)
        
        #model that is working with
        self._model = Model()
        
        # Text input for description
        self.description_input = helper.create_description_box()
        self.description_input.setPlaceholderText("Enter a description for the model...")
        # Save button
        self.save_button = helper.create_button(text = "Save Model", event = self._save_model)
        #graph data
        self._model_info = QLabel()

        button_ly = QHBoxLayout()
        button_ly.addWidget(self.save_button)
        button_ly.setAlignment(Qt.AlignRight)

        # Agregar los widgets al layout interno
        internal_layout.addWidget(self._model_info)
        internal_layout.addWidget(self.description_input)
        internal_layout.addLayout(button_ly)
        
        # Alinear todo al centro
        internal_layout.setAlignment(Qt.AlignCenter)

    @Slot(Model)
    def _update_model(self, model: Model):

        """
        This funciton updates the current model user
        is working with.
        """

        self._model = model
        print(self._model.formula)
        self._get_graph_data()

    def _get_graph_data(self):

        """
        This function updated the information of the model that is being 
        displayed and also adjusts the whole widget depending on the user's choice
        to load an already generated model or create a new one.
        """

        text = f"<b style='font-size: 16pt; color: #c2ffff'>{self._model.formula}</b><br>"  # Fórmula en negrita y tamaño grande
        text += f"<font size='6' color='#16A085'>R²: {self._model.r2:.3f}    </font>"  # R² con un color verde bonito
        text += f"<font size='6' color='#E74C3C'>MSE: {self._model.mse:.3f}</font><br>"  # MSE con un color rojo atractivo
    
        # Only loaded model have a description, if it does, we adapt the widget
        if self._model.description is not None:
            text += f"<font size='6' color='#E74C3C'>{self._model.description}</font>" 
            self.description_input.setVisible(False)
            self.save_button.setVisible(False)
        else:
            self.description_input.setText('')
            self.description_input.setVisible(True)
            self.save_button.setVisible(True)

        self._model_info.setText(text)
        font = QFont("Arial", 12, QFont.Bold)  # Cambiar la fuente a Arial, tamaño 12 y en negrita
        self._model_info.setFont(font)


    def _save_model(self):

        """
        This function acts as an event for the saving model button.
        """

        if self._model:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "Joblib Files (*.joblib)")
            if file_path:

                formula = self._model.formula
                x = self._model.x_name
                y = self._model.y_name
                r2=self._model.r2
                mse = self._model.mse
                description = self.description_input.toPlainText()
                slope = self._model.slope
                intercept = self._model.intercept

                try:
                    save_model(file_path=file_path, formula=formula, input=x, output=y,
                           r2=r2, mse=mse,description=description, slope=slope, intercept=intercept)
                    QMessageBox.information(self,"Saving Model", "Model succesfully saved")
                except Exception as e:
                    QMessageBox.information(self,"Saving model", f"Unexpected error occoured: {e}")