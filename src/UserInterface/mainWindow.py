from PySide6.QtWidgets import( 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,    
    QSizePolicy
)

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
import pandas as pd
from src.dataManagement import DataManager

from UserInterface import(ChooseColumn, 
                          ChooseFile, 
                          PrepMenu, 
                          RegressionGraph)

import UserInterface.UIHelpers as helper


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Linear Regression')
        self.setGeometry(100, 100, 1000, 550)

        self._dmanager = DataManager()

        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self._content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Create other widgets
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()  # Assuming this function returns a QWidget
        self._table.setMinimumHeight(250)
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()

        # Create the graph widget
        self._graph = RegressionGraph()  # Assuming this function returns a QWidget
        self._graph.setMinimumHeight(450)

        # Processing options layout
        self._cp_layout = QHBoxLayout()
        helper.set_layout(layout=self._cp_layout, items=[
            self._select_cols,
            self._preprocess
        ])

        # Add widgets to the main layout
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addLayout(self._cp_layout)
        self._main_layout.addWidget(self._graph)

        # Set the scroll area as the central widget
        self.setCentralWidget(scroll_area)
        self._content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Window layout
        self.setLayout(self._main_layout)
        
        # Connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data)
        self._choose_file_menu.file_selected.connect(self._table.set_data)
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)

        self._select_cols.send_selection.connect(self.show_nan_values)
        self._select_cols.selected.connect(self._preprocess.activate_menu)

        self._preprocess.preprocess_request.connect(self.handle_preprocess)
        self._preprocess.processed_data.connect(self._table.set_data)

        self._select_cols.make_regression.connect(self.handle_regression)

    @Slot(pd.DataFrame)
    def get_data(self, data):
        self._dmanager.data = data

    @Slot(int)
    def show_nan_values(self, index):
        col_name = self._dmanager.data.columns[index]
        num_nan = self._dmanager.detect(column=col_name)

        if num_nan > 0:
            QMessageBox.information(self, "Unknown Values", f'{col_name} has {num_nan} unknown values, you might want to pre-process your data.')

    @Slot()
    def handle_preprocess(self):
        columns = self._select_cols.selection()
        self._preprocess.apply_preprocess(columns=columns, manager=self._dmanager)

    @Slot()
    def handle_regression(self):
        columns = self._select_cols.selection()
        self._graph.make_regression(data=self._dmanager.data, x=columns[0], y=columns[1])
        self._graph.setVisible(True)