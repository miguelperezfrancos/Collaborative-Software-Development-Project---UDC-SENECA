"""Module for regression visualization widget implementation."""

import os
import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(REPO_ROOT)

from src.data_management import Model, save_model
import user_interface.ui_helpers as helper


class RegressionGraph(QWidget):
    """Widget class for displaying regression graphs."""


    def __init__(self):
        """Initialize the regression graph widget."""
        super().__init__()
        
        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI components."""
        # Create main container
        self.container = QWidget()
        self.container.setObjectName("container")
        
        # Set up main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        main_layout.addWidget(self.container)

        # Set up internal layout
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(10, 10, 10, 10)
        self.container.setLayout(self._layout)

        # Create and add canvas
        self.canvas = FigureCanvas(Figure())
        self._layout.addWidget(self.canvas)

    @Slot(Model)
    def make_graph(self, model: Model) -> None:
        """Create and display regression model visualization.
        
        Args:
            data: DataFrame containing the data.
            x: Name of the independent variable column.
            y: Name of the dependent variable column.
        """
        # Create regression model and get plot
        graph = model.get_plot()
        
        # Update canvas with new plot
        self.canvas.figure.clf()
        self.canvas.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.canvas.figure = graph
        self.canvas.draw()