from UserInterface import MainWindow
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
    file = QFile("src/UserInterface/stylesheet.qss")
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