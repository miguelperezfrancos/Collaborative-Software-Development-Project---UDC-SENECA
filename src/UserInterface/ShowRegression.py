from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,  # Importar QLabel para mostrar el texto
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from dataManagement.linearRegression import Regression


class RegressionGraph(QWidget):

    def __init__(self):
        super().__init__()
        
        # Crear el lienzo de Matplotlib
        self.canvas = FigureCanvas(Figure())

        # Crear un QLabel para mostrar el texto de la regresión
        self.text_label = QLabel("")

        # Configurar layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.text_label)  # Añadir el QLabel al layout
        self.setLayout(self.layout)

        self.setVisible(False)

    def make_regression(self, data, x, y):
        regression = Regression()
        regression.make_model(data, x, y)

        # Obtener la gráfica
        graph = regression.get_plot()

        # Limpiar la figura actual y asignar la nueva figura generada
        self.canvas.figure.clf()  
        self.canvas.figure = graph  
        self.canvas.draw()

        # Obtener el texto de la regresión y mostrarlo en el QLabel
        plot_text = regression.get_plot_text()
        self.text_label.setText(plot_text)  # Actualizar el texto del QLabel
