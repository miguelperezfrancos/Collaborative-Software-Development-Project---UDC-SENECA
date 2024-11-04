from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
)
import sys
import os 
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.dataManagement.linearRegression import Regression
import joblib

class RegressionGraph(QWidget):

    def __init__(self):
        super().__init__()
        
        self.canvas = FigureCanvas(Figure())
        self.regression = None
        
        # Text input for description
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter a description for the model...")

        # Label to show the description below the graph
        self.description_label = QLabel()
        
        # Save button
        self.save_button = QPushButton("Save Model")
        self.save_button.clicked.connect(self.save_model)
        self.save_button.setVisible(False)  # Initially hidden
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.description_label)
        
        # Add a horizontal layout for the save button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)
        
        # Hide the graph initially
        self.setVisible(False)
        
        # Connect input change to update description
        self.description_input.textChanged.connect(self.update_description)

    def update_description(self):
        # Update the label with the text from the input
        self.description_label.setText(self.description_input.text())

    def make_regression(self, data, x, y):
        # Create the regression model and graph
        self.regression = Regression()
        self.regression.make_model(data, x, y)
        graph = self.regression.get_plot()
        
        # Set the figure of the canvas and refresh
        self.canvas.figure = graph
        self.canvas.draw()
        
        # Show the save button
        self.save_button.setVisible(True)
        
        return self.regression._model
    
    def get_description(self):
        return self.description_input.text()

    def save_model(self):
        if self.regression and self.regression._model:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "Joblib Files (*.joblib)")
            if file_path:
                model_data = {
                    'formula': self.regression._pred_line,
                    'input_columns': list(self.regression._x_name),
                    'output_column': self.regression._y_name,
                    'r2': self.regression.get_r_squared(),
                    'mse': self.regression.get_MSE(),
                    'description': self.get_description(),
                    'model': self.regression._model
                }
                joblib.dump(model_data, file_path)
