"""Module for selecting input and output columns for regression analysis."""

# Standard library imports
import pandas as pd

# Third-party imports
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

# Local imports
from user_interface import ui_helpers as helper
from user_interface import MainWindow
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream

"""
This is the main module of the application.
In charge of running the app.
"""

def main():
    # Main entry point of the application
    app = QApplication(sys.argv)

    # Cargar el archivo QSS
    file = QFile("src/user_interface/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    
    # Create and show the main window
    interface = MainWindow()
    interface.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()