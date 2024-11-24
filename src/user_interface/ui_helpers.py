"""Provides fast, well-organized PySide6 widget creation with pre-defined 
styles.

This module contains helper functions for creating and configuring common Qt
widgets with consistent styling and behavior.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
)

from user_interface.VirtualTable import VirtualTableModel, VirtualTableView


def create_label(text: str) -> QLabel:
    """Create a styled QLabel with consistent formatting.

    Args:
        text: The text to display in the label.

    Returns:
        A configured QLabel instance.
    """
    label = QLabel(text)
    label.setFont(QFont("Arial", 12))
    label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return label


def create_button(text: str, event) -> QPushButton:
    """Create a styled QPushButton with connected event.

    Args:
        text: The button's display text.
        event: The function to call when button is clicked.

    Returns:
        A configured QPushButton instance.
    """
    button = QPushButton(text)
    button.clicked.connect(event)
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return button


def create_combo_box(default_item: str, event) -> QComboBox:
    """Create a styled QComboBox with default item and event handler.

    Args:
        default_item: The initial item to display.
        event: Function to call when selection changes.

    Returns:
        A configured QComboBox instance.
    """
    combo_box = QComboBox()
    combo_box.addItem(default_item)
    combo_box.currentIndexChanged.connect(event)
    combo_box.setMaximumWidth(400)
    return combo_box


def create_virtual_table() -> VirtualTableView:
    """Create a configured virtual table view.

    Returns:
        A configured VirtualTableView instance.
    """
    table = VirtualTableView(VirtualTableModel())
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table


def create_radio_button(text: str, event=None) -> QRadioButton:
    """Create a disabled QRadioButton with text.

    Args:
        text: The radio button's display text.
        event: Optional event handler function.

    Returns:
        A configured QRadioButton instance.
    """
    radio_button = QRadioButton(text)
    radio_button.setEnabled(False)
    return radio_button


def create_description_box() -> QTextEdit:
    """Create a styled QTextEdit for descriptions.

    Returns:
        A configured QTextEdit instance.
    """
    text_edit = QTextEdit()
    text_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    text_edit.setAlignment(Qt.AlignVCenter)
    return text_edit


def create_text_box(enabled: bool) -> QLineEdit:
    """Create a styled QLineEdit with specified enabled state.

    Args:
        enabled: Whether the text box should be enabled.

    Returns:
        A configured QLineEdit instance.
    """
    text_box = QLineEdit()
    text_box.setEnabled(enabled)
    text_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    return text_box


def set_layout(layout, items: list) -> None:
    """Add widgets or layouts to another layout.

    Args:
        layout: The parent layout to add items to.
        items: List of widgets or layouts to add.
    """
    for item in items:
        if isinstance(item, (QHBoxLayout, QVBoxLayout, QGridLayout)):
            layout.addLayout(item)
        else:
            layout.addWidget(item)


def show_error_message(message: str) -> None:
    """Display an error message dialog.

    Args:
        message: The error message to display.
    """
    error_msg = QMessageBox()
    error_msg.setIcon(QMessageBox.Critical)
    error_msg.setWindowTitle("Error")
    error_msg.setText("An error occurred!")
    error_msg.setInformativeText(message)
    error_msg.setStandardButtons(QMessageBox.Ok)
    error_msg.exec()