from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFileDialog,
)

from PySide6.QtCore import Signal
import src.UserInterface.widgetBuilder as builder


class ChooseFile(QWidget):

    """
    This class contains the module for opnening a file.
    """

    file_selected = Signal(str)

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout()

        self._file_indicator = builder.create_label(text="File path: ")
        self._path_label = builder.create_label(text="")
        self._open_file_button = builder.create_button(text="Open File Explorer", event=self.open_file_dialog)

        layout.addWidget(self._file_indicator)
        layout.addWidget(self._path_label)
        layout.addWidget(self._open_file_button)


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
                self.file_selected.emit(file_path)
            except:
                pass