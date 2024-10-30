from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)

from PySide6.QtCore import Signal, Slot
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import UserInterface.UIHelpers as helper
from dataManagement.linearRegression import Regression



class RegressionGraph(QWidget):


    def __init__(self):

        super().__init__()
        self.canvas = FigureCanvas(Figure())

        # Configurar layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)


    def make_regression(self, data, x, y):

        regression = Regression()
        regression.make_model(data, x, y)
        graph = regression.get_plot()
        
        self.canvas.figure = graph
        self.canvas.draw()