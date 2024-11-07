from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QFileDialog,
    QMessageBox
)
import sys
import os 
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.dataManagement import Model, save_model
import UserInterface.UIHelpers as helper
from PySide6.QtCore import Slot, Signal

class RegressionGraph(QWidget):

    is_model = Signal()

    def __init__(self):
        super().__init__()

        self.canvas = FigureCanvas(Figure())
        self._model = Model()

        # signal to update 
        self.is_model.connect(self._get_graph_data)
        
        # Text input for description
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter a description for the model...")
        # Save button
        self.save_button = helper.create_button(text = "Save Model", event = self._save_model)
        #graph data
        self._model_info = QLabel()
  
        
        # Add a horizontal layout for the save button
        description_layout = QVBoxLayout()
        description_layout.addWidget(self._model_info)
        description_layout.addWidget(self.description_input)
        description_layout.addWidget(self.save_button)
        
        
        # Set up layout
        self._layout = QHBoxLayout()
        self._layout.addWidget(self.canvas)
        self._layout.addLayout(description_layout)
        self.setLayout(self._layout)
        
        # Hide the graph initially
        self.setVisible(False)

    def make_regression(self, data, x, y):
        # Create the regression model and graph
        self._model.create_from_data(data, x, y)
        graph = self._model.get_plot()
        
        # Clear canvas, set new figure and refresh
        self.canvas.figure.clf()
        self.canvas.figure = graph
        self.canvas.draw()

        #clear description
        self.description_input.setText("")
        
        # Show the save button
        self.save_button.setVisible(True)
        self.is_model.emit()
    
    @Slot()
    def _get_graph_data(self):

        text = f"{self._model.formula}\nR2: {self._model.r2:.3f}\nMSE: {self._model.mse:.3f}\n"
        self._model_info.setText(text)
    
    def _get_description(self):
        return self.description_input.text()

    def _save_model(self):

        if self._model:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "Joblib Files (*.joblib)")
            if file_path:

                formula = self._model.formula
                x = self._model.x_name
                y = self._model.y_name
                r2=self._model.r2
                mse = self._model.mse
                description = self._get_description()
                slope = self._model.slope
                intercept = self._model.intercept

                try:
                    save_model(file_path=file_path, formula=formula, input=x, output=y,
                           r2=r2, mse=mse,description=description, slope=slope, intercept=intercept)
                    QMessageBox.information(self,"Saving Model", "Model succesfully saved")
                except Exception as e:
                    QMessageBox.information(self,"Saving model", f"Unexpected error occoured: {e}")