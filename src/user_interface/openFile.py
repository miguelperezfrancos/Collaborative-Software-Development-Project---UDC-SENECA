# Standard library imports
import pandas as pd

# Third-party imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
)

# Local imports
import user_interface.ui_helpers as helper
from src.data_management import FileReader, Model, load_model


class ChooseFile(QWidget):
    """A widget for selecting and loading files, such as datasets and models.

    This widget provides buttons for opening a file dialog to select a dataset
    or model and signals the selected file for further processing.

    Signals:
        file_selected: Emitted when a dataset is selected, contains pd.DataFrame
        loaded_model: Emitted when a model is loaded, contains Model instance
        hide_show: Emitted to toggle visibility of elements based on file loading
    """

    file_selected = Signal(pd.DataFrame)
    loaded_model = Signal(Model)
    hide_show = Signal(bool)

    def __init__(self):
        """Initialize the ChooseFile widget.

        Creates buttons for loading a dataset or model and displays the selected
        file path.
        """
        super().__init__()

        layout = QHBoxLayout()

        # Create UI elements
        self._file_indicator = helper.create_label(text="File path: ")
        self._path_label = helper.create_label(text="")
        self._open_dataset_button = helper.create_button(
            text="Load Dataset",
            event=self._load_dataset
        )
        self._load_model_button = helper.create_button(
            text="Load Model",
            event=self._load_model_event
        )

        # Set object names for styling
        self._file_indicator.setObjectName("filepath")
        self._path_label.setObjectName("filepath")

        # Adjust widget sizes and policies
        self._open_dataset_button.setMaximumSize(170, 50)
        self._load_model_button.setMaximumSize(170, 50)
        self._path_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        # Set layout and add widgets
        helper.set_layout(
            layout=layout,
            items=[
                self._file_indicator,
                self._path_label,
                self._open_dataset_button,
                self._load_model_button,
            ]
        )

        self.setLayout(layout)
        self.setMaximumHeight(75)

    def _load_dataset(self):
        """Open a file dialog to select and load a dataset file.

        Displays file path and processes the selected file if valid.
        Silently handles any errors that occur during file loading.
        """
        options = QFileDialog.Options()
        allowed_extensions = (
            "Compatible files (*.csv *.xlsx *.xls *.sqlite *.db)"
        )
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File: ",
            "",
            allowed_extensions,
            options=options
        )

        if file_path:
            try:
                self._path_label.setText(f"{file_path}")
                self.read_dataset(path=file_path)
            except Exception:
                pass

    def read_dataset(self, path: str):
        """Load file content into DataFrame and emit file_selected signal.

        Handles various file formats (CSV, Excel, SQLite) and potential
        errors during file processing.

        Args:
            path: The path to the file to be loaded.
        """
        reader = FileReader()

        try:
            df = reader.parse_file(path)
            self.file_selected.emit(df)
            self.hide_show.emit(True)
        except Exception as e:
            helper.show_error_message(f"ERROR: {e}")

    def _load_model_event(self):
        """Open a file dialog to select and load a model file.

        Loads the selected model, displays the file path, and emits
        the loaded_model signal. Also emits hide_show signal to adjust
        the user interface.
        """
        options = QFileDialog.Options()
        allowed_extensions = "Compatible files (*.joblib)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File: ",
            "",
            allowed_extensions,
            options=options
        )

        if file_path:
            try:
                model = load_model(file_path=file_path)
                self._path_label.setText(f"{file_path}")
                self.hide_show.emit(False)
                self.loaded_model.emit(model)
            except Exception:
                pass