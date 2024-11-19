from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
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
from PySide6.QtGui import QFont

class RegressionGraph(QWidget):

    is_model = Signal(Model)

    def __init__(self):
        
        super().__init__()

        # Crear el contenedor principal
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        main_layout.addWidget(self.container)

        # Layout interno
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(self._layout)

        self.canvas = FigureCanvas(Figure())
        self._model = Model()
          
        # Añadir el canvas al layout interno
        self._layout.addWidget(self.canvas)


    def make_regression(self, data, x, y):
        # Create the regression model and graph
        self._model.create_from_data(data, x, y)
        graph = self._model.get_plot()
        
        # Clear canvas, set new figure and refresh
        self.canvas.figure.clf()
        self.canvas.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.canvas.figure = graph
        self.canvas.draw()

        self.is_model.emit(self._model)