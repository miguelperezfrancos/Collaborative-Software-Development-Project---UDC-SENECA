import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QHeaderView  # Necessary import for handling column size
)
from PySide6.QtCore import Qt
from file_reader import FileReader, FormatError, nanoseconds
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

        # Store the selected columns
        self.input_column = None
        self.output_column = None

        # Dictionary to store the original colors of each cell
        self.original_colors = {}

        # Window settings
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        # Main vertical layout
        self.layout = QVBoxLayout()

        # Horizontal layout for file path label and open button
        self.h_layout = QHBoxLayout()

        # Label to display selected file path
        self.file_path_label = QLabel("File path: ")
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
        self.file_path_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.file_path_label2 = QLabel("")
        self.file_path_label2.setStyleSheet(""" 
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
        self.file_path_label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Button to open file explorer dialog
        self.open_button = QPushButton("Open File Explorer")
        self.open_button.clicked.connect(self.open_file_dialog)  # Connect button click to open dialog
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

        # Add label and button to the horizontal layout
        self.h_layout.addWidget(self.file_path_label)
        self.h_layout.addWidget(self.file_path_label2)
        self.h_layout.addWidget(self.open_button)

        # Add the horizontal layout to the main vertical layout
        self.layout.addLayout(self.h_layout)

        # Table to display file content
        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to expanding

        # Make columns stretch to fit the table width
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Here we make the columns take the full width

        self.layout.addWidget(self.table_widget)

        # Horizontal layout for combo boxes and confirm button
        self.h2_layout = QHBoxLayout()

        # Combo box 1 for selecting an input column
        self.combo_box1 = QComboBox()
        self.combo_box1.setStyleSheet(""" 
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.combo_box1.addItem("Select an input column")  # Default item
        self.combo_box1.currentIndexChanged.connect(self.on_combo_box1_changed)  # Connect change event
        self.h2_layout.addWidget(self.combo_box1)

        # Combo box 2 for selecting an output column
        self.combo_box2 = QComboBox()
        self.combo_box2.setStyleSheet(""" 
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.combo_box2.addItem("Select an output column")  # Default item
        self.combo_box2.currentIndexChanged.connect(self.on_combo_box2_changed)  # Connect change event
        self.h2_layout.addWidget(self.combo_box2)

        # Confirm selection button
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.clicked.connect(self.on_confirm_selection)  # Connect button click to confirm action
        self.confirm_button.setStyleSheet(""" 
            QPushButton {
                background-color: #28A745;  
                color: white;                
                font-size: 16px;            
                font-weight: bold;          
                border: none;               
                border-radius: 15px;        
                padding: 8px 20px;         
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2);  
                transition: background-color 0.3s ease;   
            }
            QPushButton:hover {
                background-color: #218838;  
            }
            QPushButton:pressed {
                background-color: #1e7e34;   
                box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); 
            }
        """)
        self.h2_layout.addWidget(self.confirm_button)

        # Add combo box layout to the main layout
        self.layout.addLayout(self.h2_layout)

        # Set main layout
        self.setLayout(self.layout)

        # Set stretch for the table to expand
        self.layout.setStretch(1, 10)  # 10: the table has more space to expand
        self.layout.setStretch(2, 1)  # 1: the combo box layout takes less space

    def open_file_dialog(self):
        # File dialog settings
        options = QFileDialog.Options()
        allowed_extensions = "Compatible files (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File: ", "", allowed_extensions, options=options)

        # If a file is selected, load it into the table
        if file_path:
            self.file_path_label2.setText(f"{file_path}")
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
            t0 = nanoseconds() #meaure displaying time
            df = reader.parse_file(file_path)

            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)

            # Check if the DataFrame is empty
            if df is None or (df.shape[0] == 0 and df.shape[1] == 0):
                raise ValueError("Empty File")
            
            # Reset the dictionary of original colors
            self.original_colors = {}

            # If DataFrame has content, populate the table and combo boxes
            if df.shape[0] > 0 and df.shape[1] > 0:
                # Populate the table with the data from the DataFrame
                self.table_widget.setRowCount(df.shape[0])
                self.table_widget.setColumnCount(df.shape[1])
                self.table_widget.setHorizontalHeaderLabels(df.columns)

                # Fill the table with the DataFrame content and store the original colors
                for i in range(df.shape[0]):
                    for j in range(df.shape[1]):
                        item = QTableWidgetItem(str(df.iat[i, j]))
                        self.table_widget.setItem(i, j, item)

                        # Store original background and foreground colors
                        self.original_colors[(i, j)] = (item.background(), item.foreground())

                # Populate combo boxes with column names
                self.combo_box1.clear()
                self.combo_box1.addItem("Select an input column")
                self.combo_box1.addItems(df.columns)

                self.combo_box2.clear()
                self.combo_box2.addItem("Select an output column")
                self.combo_box2.addItems(df.columns)

                # Reset previously selected columns
                self.input_column = None
                self.output_column = None
            else:
                raise ValueError("Reading Error.")
            
            tf = nanoseconds()
            print(f'displaying time: {(tf-t0) / 1000000} miliseconds')

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

    def on_combo_box1_changed(self, index):
        if index > 0:  # Ensure valid input column is selected
            column = index - 1

            # Check if column is the same as combo_box2
            if column == self.output_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self.combo_box1.setCurrentIndex(0)  # Reset combo_box1 selection
            else:
                self.highlight_column(self.input_column, column, Qt.yellow)
                self.input_column = column

    def on_combo_box2_changed(self, index):
        if index > 0:  # Ensure valid output column is selected
            column = index - 1

            # Check if column is the same as combo_box1
            if column == self.input_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self.combo_box2.setCurrentIndex(0)  # Reset combo_box2 selection
            else:
                self.highlight_column(self.output_column, column, Qt.cyan)
                self.output_column = column

    def highlight_column(self, previous_column, new_column, color):
        # Reset previous column to original colors
        if previous_column is not None:
            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, previous_column)
                if item:
                    original_background, original_foreground = self.original_colors[(row, previous_column)]
                    item.setBackground(original_background)
                    item.setForeground(original_foreground)

        # Highlight new column
        if new_column is not None:
            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, new_column)
                if item:
                    item.setBackground(color)
                    item.setForeground(Qt.black)

    def on_confirm_selection(self):
        # Perform the action you want after confirming the selection
        if self.input_column is not None and self.output_column is not None:
            QMessageBox.information(self, "Selection Confirmed", f"Input Column: {self.input_column + 1}, Output Column: {self.output_column + 1}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select two different columns before confirming.")


if __name__ == "__main__":
    # Main entry point of the application
    app = QApplication(sys.argv)

    # Create and show the FileExplorer widget
    explorer = FileExplorer()
    explorer.show()

    # Start the application's event loop
    sys.exit(app.exec())