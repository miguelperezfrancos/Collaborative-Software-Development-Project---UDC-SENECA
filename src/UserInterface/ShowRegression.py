from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dataManagement.linearRegression import Regression


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
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.description_input)
        self.layout.addWidget(self.description_label)
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
        
        return self.regression.model

    def get_formula(self):
        if self.regression and self.regression.model:
            coef = self.regression.model.coef_
            intercept = self.regression.model.intercept_
            formula = f"y = {intercept:.4f}"
            for i, col in enumerate(self.regression.X.columns):
                formula += f" + {coef[i]:.4f} * {col}"
            return formula
        return ""

    def get_description(self):
        return self.description_input.text()