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
    QRadioButton
)

from UserInterface.VirtualTable import VirtualTableModel, VirtualTableView

def create_label(text: str) -> QLabel:

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
        
def create_button(text: str, event) -> QPushButton:

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
        }""")
    
    return button
        
def create_combo_box(default_item, event) -> QComboBox:

    combo_box = QComboBox()
    combo_box.setStyleSheet("""
        QComboBox {
            padding: 8px;
            font-size: 14px;
        }""")
    
    combo_box.addItem(default_item)
    combo_box.currentIndexChanged.connect(event)
    return combo_box

def create_virtual_table():

    table = VirtualTableView(VirtualTableModel())
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table

def create_radio_button(text:str, event=None) -> QRadioButton:

    radio_button = QRadioButton(text)
    return radio_button