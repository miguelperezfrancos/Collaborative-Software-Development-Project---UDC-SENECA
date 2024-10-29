from UserInterface.main_window_two import MainWindow
import sys
from PySide6.QtWidgets import QApplication

"""
This is the main module of the application.
In charge of running the app.
"""

def main():
    # Main entry point of the application
    app = QApplication(sys.argv)

    # Create and show the main window
    interface = MainWindow()
    interface.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()