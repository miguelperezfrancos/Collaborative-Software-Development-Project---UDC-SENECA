"""Module for preprocessing menu widget implementation."""

from data_management.dataManager import DataManager

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QMessageBox,
    QButtonGroup,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Signal, Slot, Qt
import pandas as pd
import user_interface.ui_helpers as helper


class PrepMenu(QWidget):
    """Widget class for preprocessing options menu."""

    preprocess_request = Signal()
    processed_data = Signal(pd.DataFrame)

    def __init__(self):
        """Initialize the preprocessing menu widget."""
        super().__init__()
        self._manager = DataManager()

        # Declare layouts
        main_layout = QVBoxLayout()
        self._buttons_layout = QHBoxLayout()
        self._opts_layout = QGridLayout()

        self._setup_ui_elements()
        self._setup_button_group()
        self._setup_signals()
        self._build_layout(main_layout)

        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

    def _setup_ui_elements(self):
        """Set up UI elements of the preprocessing menu."""
        self._title = helper.create_label(text="Preprocessing options")
        self._title.setObjectName('title')
        
        self._remove_option = helper.create_radio_button(
            text='Remove row')
        self._constant_option = helper.create_radio_button(
            text='Replace with a number')
        self._mean_option = helper.create_radio_button(
            text='Replace with mean')
        self._median_option = helper.create_radio_button(
            text='Replace with median')
        
        self._input_number = helper.create_text_box(enabled=False)
        self._input_number.setVisible(False)
        
        self._apply_button = helper.create_button(text='Apply', 
                                                event=self.on_apply_button)
        self._apply_button.setEnabled(False)

    def _setup_button_group(self):
        """Set up button group for radio buttons."""
        self._preprocessing_opts = QButtonGroup()
        for button in [
            self._remove_option,
            self._constant_option,
            self._mean_option,
            self._median_option
        ]:
            self._preprocessing_opts.addButton(button)

    def _setup_signals(self):
        """Connect widget signals."""
        self._constant_option.toggled.connect(self.toggle_input)

    def _build_layout(self, main_layout):
        """Build the widget layout."""
        title_layout = QHBoxLayout()
        title_layout.addWidget(self._title)

        self._opts_layout.setHorizontalSpacing(2)
        self._opts_layout.setVerticalSpacing(10)

        # Add widgets to options layout
        self._opts_layout.addWidget(self._constant_option, 0, 0)
        self._opts_layout.addWidget(self._input_number, 0, 1)
        self._opts_layout.addWidget(self._mean_option, 1, 0)
        self._opts_layout.addWidget(self._median_option, 2, 0)
        self._opts_layout.addWidget(self._remove_option, 3, 0)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self._apply_button)
        button_layout.setAlignment(Qt.AlignBottom)

        self._buttons_layout.addLayout(self._opts_layout)
        self._buttons_layout.addLayout(button_layout)

        helper.set_layout(
            layout=main_layout,
            items=[title_layout, self._buttons_layout]
        )

    @Slot(bool)
    def activate_menu(self, enabled: bool):
        """Enable or disable menu elements.
        
        Args:
            enabled: Boolean indicating if menu should be enabled.
        """
        for button in [
            self._constant_option,
            self._mean_option,
            self._median_option,
            self._remove_option,
            self._apply_button
        ]:
            button.setEnabled(enabled)

        self.toggle_input(checked=False)
        
        # Reset button group selection
        self._preprocessing_opts.setExclusive(False)
        for button in self._preprocessing_opts.buttons():
            button.setChecked(False)
        self._preprocessing_opts.setExclusive(True)

    @Slot(bool)
    def toggle_input(self, checked: bool):
        """Enable and set visible the input field for constant value option.
        
        Args:
            checked: Boolean indicating if constant value option is selected.
        """
        self._input_number.setEnabled(checked)
        self._input_number.setVisible(checked)
        self._input_number.setText('')

    def on_apply_button(self):
        """Handle apply button click."""
        self.preprocess_request.emit()

    def apply_preprocess(self, columns, manager: DataManager):
        """Apply selected preprocessing operation.
        
        Args:
            columns: List of columns to preprocess.
            manager: DataManager instance to perform operations.
        """
        choice = self._preprocessing_opts.checkedButton()
        
        try:
            if choice is self._remove_option:
                manager.delete(columns=columns)
            elif choice is self._mean_option:
                manager.replace(columns=columns)
            elif choice is self._median_option:
                manager.replace(columns=columns, value='median')
            elif choice is self._constant_option:
                constant_value = float(self._input_number.text())
                manager.replace(columns=columns, value=constant_value)

            self.processed_data.emit(manager.data)
            QMessageBox.information(
                self,
                "Successful preprocess",
                f"{columns[0]} and {columns[1]} no longer have null values"
            )

        except Exception as e:
            helper.show_error_message(
                message=f"Preprocess could not be completed: {e}"
            )