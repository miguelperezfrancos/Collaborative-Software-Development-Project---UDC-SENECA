from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFileDialog
)

from PySide6.QtCore import Signal
import UserInterface.UIHelpers as helper
from dataManagement.fileReader import FileReader
import pandas as pd


class ChooseFile(QWidget):

    """
    This class contains the module for opnening a file.
    """

    file_selected = Signal(pd.DataFrame)

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout()

        self._file_indicator = helper.create_label(text="File path: ")
        self._path_label = helper.create_label(text="")
        self._open_file_button = helper.create_button(text="Open File Explorer", event=self.open_file_dialog)

        helper.set_layout(layout=layout, items=[
            self._file_indicator,
            self._path_label,
            self._open_file_button
        ])

        self.setLayout(layout)


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
                self._path_label.setText(f"{file_path}")
                self.load_file(path=file_path)
            except:
                pass

    def load_file(self, path: str):

        """
        Loads the content of the file at the given path into the table widget.
        Handles different file formats (e.g., CSV, Excel, SQLite) and errors
        such as unsupported formats, empty files, or parsing issues.

        It also sends file to the data manager class and stablishe the data as
        the current model for the virtual table.

        Parameters:
            file_path (str): The path to the file to be loaded.
        """

        reader = FileReader()

        try:
            df = reader.parse_file(path)
            self.file_selected.emit(df)

        except:  # Catch any other unknown errors
            self._show_error_message('ERROR: Unknown error')    