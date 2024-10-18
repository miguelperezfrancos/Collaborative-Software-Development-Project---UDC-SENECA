import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt
from file_reader import FileReader, FormatError
import pandas as pd  
import sqlite3

class FileExplorer(QWidget):
    
    """
    FileExplorer class represents a graphical user interface (GUI) that allows
    users to select a file, read its content, and display it in a table. The class
    provides error handling for various types of file and format errors.
    """
    
    def __init__(self):
        """
        Initializes the FileExplorer widget, setting up the layout and components
        such as the file explorer button, file path label, and table widget.
        """
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        # Main layout for the widget
        self.layout = QVBoxLayout()

        # Button to open the file explorer dialog
        self.open_button = QPushButton("Open File Explorer")
        self.open_button.clicked.connect(self.open_file_dialog)

        # Set style for the button
        self.open_button.setStyleSheet(""" 
            QPushButton {
                background-color: #007BFF;  
                color: white;                
                font-size: 18px;            
                font-weight: bold;          
                border: none;               
                border-radius: 20px;        
                padding: 12px 30px;         
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);  
                transition: background-color 0.3s ease;   
            }
            QPushButton:hover {
                background-color: #0056b3;  
            }
            QPushButton:pressed {
                background-color: #003d80;   
                box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5); 
            }
        """)

        # Add the button to the layout
        self.layout.addWidget(self.open_button)

        # Label to display the selected file path
        self.file_path_label = QLabel("File path: ")
        
        # Set style for the file path label
        self.file_path_label.setStyleSheet(""" 
            QLabel {
                background-color: #FFFDD0;  
                color: #333;                
                font-size: 14px;           
                font-weight: bold;         
                border: 1px solid #d1d1d1; 
                border-radius: 7px;      
                padding: 8px;             
                margin-top: 5px;          
            }
        """)
        
        self.file_path_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.layout.addWidget(self.file_path_label)
        
        # Table widget to display the file content
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Spacer to fill empty space at the bottom
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the main layout
        self.setLayout(self.layout)

    def open_file_dialog(self):
        """
        Opens a file dialog for the user to select a file. Only files with certain
        extensions are allowed. The selected file path is displayed in the label,
        and the file content is loaded into the table.
        """
        options = QFileDialog.Options()
        allowed_extensions = "Supported files (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file:", "", allowed_extensions, options=options)
        
        # If a file was selected, load the file and display its content
        if file_path:
            self.file_path_label.setText(f"Selected file path: {file_path}")
            self.load_file(file_path)

    def load_file(self, file_path):
        """
        Loads the content of the file at the given path into the table widget.
        Handles different file formats (e.g., CSV, Excel, SQLite) and errors
        such as unsupported formats, empty files, or parsing issues.

        Parameters:
            file_path (str): The path to the file to be loaded.
        """
        reader = FileReader()
        try:
            # Attempt to read the file using the FileReader
            df = reader.parse_file(file_path)

            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            # Check if the DataFrame is empty
            if df is None or (df.shape[0] == 0 and df.shape[1] == 0):
                raise ValueError("Empty File")

            if df.shape[0] > 0 and df.shape[1] > 0:
                # Populate the table with the data from the DataFrame
                self.table_widget.setRowCount(df.shape[0])
                self.table_widget.setColumnCount(df.shape[1])
                self.table_widget.setHorizontalHeaderLabels(df.columns)

                # Fill the table with the DataFrame's content
                for i in range(df.shape[0]):
                    for j in range(df.shape[1]):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
            else:
                raise ValueError("Reading Error.")

        # Catch specific errors and display error messages
        except FormatError:
            self.show_error_message('ERROR: Unsupported file format')
        except pd.errors.EmptyDataError:
            self.show_error_message('ERROR: This file might be empty or corrupted')
        except pd.errors.ParserError:
            self.show_error_message('ERROR: This file could not be parsed')
        except sqlite3.DatabaseError:
            self.show_error_message("ERROR: An error occurred with your database")
        except sqlite3.OperationalError:
            self.show_error_message('ERROR: Could not access the database')
        except FileNotFoundError:
            self.show_error_message('ERROR: File not found')
        except:  # Catch any other unknown errors
            self.show_error_message('ERROR: Unknown error')    

    def show_error_message(self, message):
        """
        Displays an error message dialog.

        Parameters:
            message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

if __name__ == "__main__":
    # Main entry point of the application
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.show()
    sys.exit(app.exec())