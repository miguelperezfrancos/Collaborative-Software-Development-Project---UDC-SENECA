"""Module for selecting input and output columns for regression analysis."""

# Standard library imports
import pandas as pd

# Third-party imports
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

# Local imports
import src.user_interface.ui_helpers as helper


class ChooseColumn(QWidget):
    """Widget for selecting input and output columns for regression analysis.

    Provides combo boxes for column selection and a button to generate a
    regression model. Emits signals for communication with other components.

    Signals:
        send_selection: Signal for checking NaN values (int)
        selected: Signal indicating valid selection made (bool)
        make_regression: Signal to trigger regression model creation
    """

    send_selection = Signal(int)
    selected = Signal(bool)
    make_regression = Signal()

    def __init__(self):
        """Initialize the widget with selection menus and generate button."""
        super().__init__()
        
        layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        
        self._title = helper.create_label(text='Column selection')
        self._title.setObjectName('title')
        
        self._input_menu = helper.create_combo_box(
            default_item="Select an input column",
            event=self.on_combo_box1_changed
        )
        
        self._output_menu = helper.create_combo_box(
            default_item="Select an output column",
            event=self.on_combo_box2_changed
        )
        
        self.create_model = helper.create_button(
            text="Generate model",
            event=self.on_create_model
        )
        
        self.selected.connect(self.enable_button)

        # Arrange UI elements
        title_layout.addWidget(self._title)
        title_layout.setAlignment(Qt.AlignCenter)

        helper.set_layout(
            layout=layout,
            items=[
                title_layout,
                self._input_menu,
                self._output_menu
            ]
        )

        layout.setAlignment(Qt.AlignTop)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    @Slot(pd.DataFrame)
    def update_selection(self, data):
        """Update combo boxes with column names from the data.

        Args:
            data: DataFrame containing columns to populate combo boxes.
        """
        items = data.columns
        menu_defaults = {
            self._input_menu: 'Select an input column',
            self._output_menu: 'Select an output column'
        }

        for menu, default in menu_defaults.items():
            menu.clear()
            menu.addItem(default)
            menu.addItems(items)

    def check_selection(self, menu):
        """Verify that different columns are selected for input and output.

        Args:
            menu: The combo box that triggered this check.
        """
        if self._input_menu.currentText() == self._output_menu.currentText():
            QMessageBox.warning(
                self,
                "Error",
                "You cannot select the same column."
            )
            menu.setCurrentIndex(0)
        else:
            self.selected.emit(True)

    def selection(self):
        """Return the currently selected input and output columns.

        Returns:
            List containing names of selected input and output columns.
        """
        return [
            self._input_menu.currentText(),
            self._output_menu.currentText()
        ]

    def on_combo_box1_changed(self, index):
        """Handle changes in the input column selection.

        Args:
            index: Index of the selected item in the input combo box.
        """
        if index != 0:
            self.send_selection.emit(index - 1)
            if self._output_menu.currentIndex() != 0:
                self.check_selection(menu=self._input_menu)
        else:
            self.selected.emit(False)

    def on_combo_box2_changed(self, index):
        """Handle changes in the output column selection.

        Args:
            index: Index of the selected item in the output combo box.
        """
        if index != 0:
            self.send_selection.emit(index - 1)
            if self._input_menu.currentIndex() != 0:
                self.check_selection(menu=self._output_menu)
        else:
            self.selected.emit(False)

    @Slot(bool)
    def enable_button(self, enabled):
        """Enable or disable the create model button.

        Args:
            enabled: Whether the button should be enabled.
        """
        self.create_model.setEnabled(enabled)

    def on_create_model(self):
        """Emit signal to create regression model."""
        self.make_regression.emit()
