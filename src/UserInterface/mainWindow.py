import sys

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QComboBox
)

from PySide6.QtCore import Qt
from dataManagement.fileReader import FileReader
import pandas as pd  
import UserInterface.widgetBuilder as builder

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

        #set window dimensions
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        #declare layouts
        self._main_layout = QVBoxLayout()
        self._hor_1 = QHBoxLayout()
        self._hor_2 = QHBoxLayout()

        #declare widgets
        self._file_indicator = builder.create_label(text="File path: ")
        self._path_label = builder.create_label(text="")
        self._open_file_button = builder.create_button(text="Open File Explorer", event=self.open_file_dialog)
        self._input_menu = builder.create_combo_box(default_item= "Select an input column", event=self.on_combo_box1_changed)
        self._output_menu = builder.create_combo_box(default_item="Select an output column", event=self.on_combo_box2_changed)
        self._confirm_cols_button = builder.create_button(text="Confirm Selection", event=self.on_confirm_selection)
        self._table = builder.create_virtual_table()

        #set up layouts
        self._set_layout(layout = self._hor_1, items=[self._file_indicator, self._path_label, self._open_file_button])
        self._set_layout(layout = self._hor_2, items=[self._input_menu, self._output_menu, self._confirm_cols_button])
        self._set_layout(layout = self._main_layout, items=[self._hor_1, self._table, self._hor_2])

        self._hor_2.setStretch(1, 10)  # Table expands
        self._hor_2.setStretch(2, 1)   # Combo box layout takes less space

        self.setLayout(self._main_layout)
        self.original_colors = {}

    def _set_layout(self, layout, items: list):

        """
        Authomatically adds widget or layout to another layout.
        """
        
        for i in items:
            if isinstance(i, QHBoxLayout) or isinstance(i, QVBoxLayout):
                layout.addLayout(i)
            else:
                layout.addWidget(i)

    def _show_error_message(self, message):
        """
        Displays an error message dialog.

        Parameters:
            message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

    def _load_file(self, file_path):

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
            self._table.model().setDataFrame(df)

        except:  # Catch any other unknown errors
            self._show_error_message('ERROR: Unknown error')    


        # Update regression entry menu
        self._change_column_selection(menu=self._input_menu, items=df.columns,
                                      default_msg='Select an input column')
        
        self._change_column_selection(menu=self._output_menu, items=df.columns, 
                                      default_msg='Select an output column')

        # Reset previously selected columns
        self.input_column = None
        self.output_column = None

    def _change_column_selection(self, menu: QComboBox, items, default_msg: str):

        menu.clear()
        menu.addItem(default_msg)
        menu.addItems(items)

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
                self._load_file(file_path)
                self._path_label.setText(f"{file_path}")
            except:
                pass
            
    def on_combo_box1_changed(self, index):

        if index > 0:  # Ensure valid input column is selected
            column = index - 1

            # Check if column is the same as combo_box2
            if column == self.output_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self._input_menu.setCurrentIndex(0)  # Reset combo_box1 selection
            else:
                self._input_column = column

    def on_combo_box2_changed(self, index):

        if index > 0:  # Ensure valid output column is selected

            column = index - 1

            # Check if column is the same as combo_box1
            if column == self._input_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self._output_menu.setCurrentIndex(0)  # Reset combo_box2 selection
            else:
                self._output_column = column

    def on_confirm_selection(self):

        # Perform the action you want after confirming the selection
        if self._input_column is not None and self._output_column is not None:
            QMessageBox.information(self, "Selection Confirmed", f"Input Column: {self._input_column + 1}, Output Column: {self._output_column + 1}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select two different columns before confirming.")
