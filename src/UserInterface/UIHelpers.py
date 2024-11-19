"""
This module will provide a fast, well-organised pySide6
widget cretion with a pre-defined style to build the user
interface.
"""

from  PySide6.QtWidgets import (
    QPushButton,
    QLabel,
    QSizePolicy,
    QComboBox,
    QHeaderView,
    QRadioButton,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QTextEdit
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from UserInterface.VirtualTable import VirtualTableModel, VirtualTableView

def create_label(text: str) -> QLabel:

    label = QLabel(text)
    label.setFont(QFont("Arial", 12))  # Fuente similar a Chrome
    label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return label

        
def create_button(text: str, event) -> QPushButton:

    button = QPushButton(text)
    button.clicked.connect(event)
    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    return button
        
def create_combo_box(default_item, event) -> QComboBox:

    combo_box = QComboBox()
    combo_box.addItem(default_item)
    combo_box.currentIndexChanged.connect(event)
    combo_box.setMaximumWidth(400)
    return combo_box

def create_virtual_table():

    table = VirtualTableView(VirtualTableModel())
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table

def create_radio_button(text:str, event=None) -> QRadioButton:

    radio_button = QRadioButton(text)
    radio_button.setEnabled(False)
    return radio_button

def create_description_box() -> QTextEdit:

    textEdit = QTextEdit()
    textEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    textEdit.setAlignment(Qt.AlignVCenter)  # Centrar el texto verticalmente

    return textEdit

def create_text_box() -> QLineEdit:

    text_box = QLineEdit()
    text_box.setEnabled(False)
    text_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
   
    return text_box

def set_layout(layout, items: list):

    """
    Automatically adds widget or layout to another layout.

    Parameters:
        layout: layout that will contain the widgets or another layouts.
        items (list): list of items that will be stored in the layout.
    """
        
    for i in items:
        if isinstance(i, QHBoxLayout) or isinstance(i, QVBoxLayout):
            layout.addLayout(i)
        else:
            layout.addWidget(i)

def show_error_message(message: str):
        
        """
        This method launches an error message.
        """
        # Create the message box
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)  # Set the icon to "Critical" for an error
        error_msg.setWindowTitle("Error")
        error_msg.setText("An error occurred!")
        error_msg.setInformativeText(f'{message}')
        error_msg.setStandardButtons(QMessageBox.Ok)  # Add the OK button
        error_msg.exec()  # Display the message box