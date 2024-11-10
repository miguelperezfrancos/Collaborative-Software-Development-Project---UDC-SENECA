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
from src.dataManagement import DataManager, Model

from src.UserInterface import(ChooseColumn, 
                          ChooseFile, 
                          PrepMenu, 
                          RegressionGraph,
                          RepModel)

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
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()
        self._loaded_model = RepModel()
        self._graph = RegressionGraph()
        
        # specify some requirements
        self._table.setMinimumHeight(250)
        self._graph.setMinimumHeight(450)
        self._loaded_model.setVisible(False)

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
        self._main_layout.addWidget(self._loaded_model)

        # Set the scroll area as the central widget
        self.setCentralWidget(scroll_area)
        self._content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Window layout
        self.setLayout(self._main_layout)
        
        # Connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data)
        self._choose_file_menu.file_selected.connect(self._table.set_data)
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)
        self._choose_file_menu.loaded_model.connect(self.update_model)
        self._choose_file_menu.hide_show.connect(self.hide_show_data)

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
        """
        This fucntion is activated when user generates regression, and it provides
        preprocessing module the necessary data.
        """
        columns = self._select_cols.selection()
        self._preprocess.apply_preprocess(columns=columns, manager=self._dmanager)

    @Slot()
    def handle_regression(self):
        """
        This fucntion is activated when user generates regression, and it provides
        regression module the necessary data.
        """
        columns = self._select_cols.selection()
        self._graph.make_regression(data=self._dmanager.data, x=columns[0], y=columns[1])
        self._graph.setVisible(True)

    @Slot(bool)
    def hide_show_data(self, show: bool):

        """
        This function shows or hide widgets according
        to what type of file is loaded by user.
        """

        self._table.setVisible(show)
        self._select_cols.setVisible(show)
        self._preprocess.setVisible(show)
        self._graph.setVisible(False)
        self._loaded_model.setVisible(not show)


    @Slot(Model)
    def update_model(self, model: Model):
        """
        This function provides our model representation widget
        the model that is loaded.
        """
        self._loaded_model.model = model
        self._loaded_model.update_model()