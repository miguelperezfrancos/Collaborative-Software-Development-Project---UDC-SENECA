import sys
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QSizePolicy,
    QMessageBox,
    QComboBox,
    QHeaderView
)

from PySide6.QtCore import Qt
from fileReader import FileReader, FormatError
import pandas as pd  
import sqlite3
from VirtualTable import VirtualTableView, VirtualTableModel

class MainWindow(QWidget):
    
    """
    FileExplorer class represents a graphical user interface (GUI) that allows
    users to select a file, read its content, and display it in a table. The class
    provides error handling for various types of file and format errors.
    """
    
    def __init__(self):
        
        super().__init__()

        # Store the selected columns
        self._input_column = None
        self._output_column = None

        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        self._layout = QVBoxLayout() # Main layout
        self._h_layout = QHBoxLayout() # Horizontal layout for file path label and open button       
        self._h2_layout = QHBoxLayout()  # Horizontal layout for combo boxes and confirm button

        self._create_widgets()
        self._set_up_layout()
        self.setLayout(self._layout)

        self.original_colors = {}


    def _create_widgets(self):

        self.file_path_label = self._create_label("File path: ")
        self.file_path_label2 = self._create_label("")

        self.open_button = self._create_button("Open File Explorer", self.open_file_dialog)
        
        self.combo_box1 = self._create_combo_box("Select an input column", self.on_combo_box1_changed)
        self.combo_box2 = self._create_combo_box("Select an output column", self.on_combo_box2_changed)

        self.confirm_button = self._create_button("Confirm Selection", self.on_confirm_selection)

        self.table_widget = VirtualTableView(VirtualTableModel())
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _create_label(self, text):

        label = QLabel(text)

        label.setStyleSheet("""
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

        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        return label
        
    def _create_button(self, text, event):

        button = QPushButton(text)
        button.clicked.connect(event)

        button.setStyleSheet("""
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
        return button
        
    def _create_combo_box(self, default_item, event):

        combo_box = QComboBox()
        combo_box.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
        """)
        combo_box.addItem(default_item)
        combo_box.currentIndexChanged.connect(event)
        return combo_box

    def _set_up_layout(self):

        self._h_layout.addWidget(self.file_path_label)
        self._h_layout.addWidget(self.file_path_label2)
        self._h_layout.addWidget(self.open_button)

        self._layout.addLayout(self._h_layout)
        self._layout.addWidget(self.table_widget)

        self._h2_layout.addWidget(self.combo_box1)
        self._h2_layout.addWidget(self.combo_box2)
        self._h2_layout.addWidget(self.confirm_button)

        self._layout.addLayout(self._h2_layout)
        self._layout.setStretch(1, 10)  # Table expands
        self._layout.setStretch(2, 1)   # Combo box layout takes less space


        










    def open_file_dialog(self):

        """
        This function defines the events that will take place
        if user clicks Open File button.
        """

        #Gestión de errores: el archivo no se puede abrir o está corrupto

        # File dialog settings
        options = QFileDialog.Options()
        allowed_extensions = "Compatible files (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File: ", "", allowed_extensions, options=options)

        # If a file is selected, load it into the table
        if file_path:

            try:
                self.load_file(file_path)
                self.file_path_label2.setText(f"{file_path}")
            except:
                pass
            
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
            df = reader.parse_file(file_path)
            self.table_widget.model().setDataFrame(df)

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
        if self._input_column is not None and self.output_column is not None:
            QMessageBox.information(self, "Selection Confirmed", f"Input Column: {self._input_column + 1}, Output Column: {self._output_column + 1}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select two different columns before confirming.")
