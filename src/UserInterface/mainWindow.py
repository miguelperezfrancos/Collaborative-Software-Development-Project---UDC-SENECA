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
from UserInterface.predictions import Predict


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Linear Regression')
        self.setGeometry(100, 100, 1000, 550)

        self._dmanager = DataManager()

        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)
        self._content_widget.setObjectName("contentWidget")


        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self._content_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Create other widgets
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()  # Assuming this function returns a QWidget
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()
        self._model_info = RepModel()
        self._graph = RegressionGraph()
        self._predict = Predict()

        self._model_info.setVisible(False)
        self._graph.setVisible(False)
        
        # specify some requirements
        self._table.setMinimumHeight(250)
        self._graph.setMinimumHeight(450)

        # Processing options layout
        self._cp_layout = QHBoxLayout()
        helper.set_layout(layout=self._cp_layout, items=[
            self._select_cols,
            self._preprocess
        ])

        #layout for model representation
        self._model_layout = QVBoxLayout()
        helper.set_layout(layout=self._model_layout, items=[
            self._model_info,
            self._predict
        ])

        self._model_two_layout = QHBoxLayout()
        helper.set_layout(layout= self._model_two_layout, items=[
            self._graph,
            self._model_layout
        ])

        #layout for create model button
        self._gen_button_ly = QHBoxLayout()
        self._gen_button_ly.addWidget(self._select_cols.create_model)
        self._gen_button_ly.setAlignment(Qt.AlignCenter)


        # Add widgets to the main layout
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addLayout(self._cp_layout)
        self._main_layout.addLayout(self._gen_button_ly)
        self._main_layout.addLayout(self._model_two_layout)

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)
        self._content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Window layout
        self.setLayout(self._main_layout)
        
        # Connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data)
        self._choose_file_menu.file_selected.connect(self._table.set_data)
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)
        self._choose_file_menu.hide_show.connect(self.hide_show_data) # hide or show widgets

        self._select_cols.send_selection.connect(self.show_nan_values)
        self._select_cols.selected.connect(self._preprocess.activate_menu)

        self._preprocess.preprocess_request.connect(self.handle_preprocess)
        self._preprocess.processed_data.connect(self._table.set_data)

        self._graph.is_model.connect(self._model_info._update_model) # display model info when model in generated
        self._choose_file_menu.loaded_model.connect(self._model_info._update_model) # display model info when model is loaded

        self._graph.is_model.connect(self._predict.update_model) # display model info when model in generated
        self._choose_file_menu.loaded_model.connect(self._predict.update_model) # display model info when model is loaded

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
        This function is activated when user generates regression, and it provides
        regression module the necessary data.
        """
        columns = self._select_cols.selection()

        num_nan = 0
        num_nan += self._dmanager.detect(columns[0])
        num_nan += self._dmanager.detect(columns[1])

        if num_nan == 0:

            pix = self._graph.canvas.devicePixelRatioF()

            try:
                self._graph.make_regression(data=self._dmanager.data, x=columns[0], y=columns[1])
                self._graph.setVisible(True)
                self._model_info.setVisible(True)
                self._predict.setVisible(True)
            except Exception as e:
                helper.show_error_message(f'Unexpected error: {e}')
                self._graph.setVisible(False)
                self._model_info.setVisible(False)
                self._predict.setVisible(False)

        else:
            helper.show_error_message(f'Data contains NaN values: please, apply preeprofess before generating model.')

    @Slot(bool)
    def hide_show_data(self, show: bool):

        """
        This function shows or hide widgets according
        to what type of file is loaded by user.
        """

        self._table.setVisible(show)
        self._select_cols.setVisible(show)
        self._preprocess.setVisible(show)
        self._preprocess.toggle_input(checked=False)
        self._select_cols.create_model.setVisible(show) # generate model button
        self._graph.setVisible(False)
        self._model_info.setVisible(not show)
        self._predict.setVisible(not show)