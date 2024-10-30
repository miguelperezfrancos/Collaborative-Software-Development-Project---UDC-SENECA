from PySide6.QtWidgets import( 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,    
    QSizePolicy,
    QSpacerItem
)

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
import pandas as pd
from dataManagement.dataManager import DataManager

from UserInterface import(ChooseColumn, 
                          ChooseFile, 
                          PrepMenu, 
                          RegressionGraph)

import UserInterface.UIHelpers as helper


class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()

        self.setWindowTitle('Rodri es gay')
        self.setGeometry(100, 100, 1000, 500)

        self._dmanager = DataManager()

        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)

        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(self._content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Desactivar el scroll horizontal
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Crear otros widgets
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()  # Suponiendo que esta función devuelve un QWidget
        self._table.setMinimumHeight(250)
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()

        # Crear el gráfico
        self._graph = RegressionGraph()  # Suponiendo que esta función devuelve un QWidget
        self._graph.setMinimumHeight(350)

        # Layout de opciones de procesamiento
        self._cp_layout = QHBoxLayout()
        helper.set_layout(layout=self._cp_layout, items=[
            self._select_cols,
            self._preprocess
        ])



        # Agregar widgets al layout principal
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addLayout(self._cp_layout)
        self._main_layout.addWidget(self._graph)

        # Establecer el área de scroll como el widget central
        self.setCentralWidget(scroll_area)
        self._content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout de la ventana principal
        self.setLayout(self._main_layout)
        
        # connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data) # send selected file to data manager
        self._choose_file_menu.file_selected.connect(self._table.set_data) # send data to table
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection) # send data to column selection menu

        self._select_cols.send_selection.connect(self.show_nan_values) # get selected column to check if it has NaN values
        self._select_cols.selected.connect(self._preprocess.activate_menu) # send selection status to activate preprocess menu

        self._preprocess.preprocess_request.connect(self.handle_preprocess) # handle preprocessing
        self._preprocess.processed_data.connect(self._table.set_data) # update table content when preprocess is done

        self._select_cols.make_regression.connect(self.handle_regression) # stablish connection to create regression graph
        

    @Slot(pd.DataFrame)
    def get_data(self, data):
        self._dmanager.data = data


    @Slot(int)
    def show_nan_values(self, index):

        """
        This function checks if a column of the data frame has NaN values, if it does,
        it will inform the user about it raising an informative message.

        Parameters:
            col_name: name o fthe column in the data frame.
        """

        col_name = self._dmanager.data.columns[index]
        num_nan = self._dmanager.detect(column=col_name)

        if num_nan > 0:
            QMessageBox.information(self, "Unknown Values", f'{col_name} has {num_nan} unknown values, you might want to pre-process your data.')


    @Slot()
    def handle_preprocess(self):
        """
        Esta function llama al método de preprocesado de datos
        cuando el botón de apply preprocess es presionado (este
        emite una señal)
        """
        columns = self._select_cols.selection()
        self._preprocess.apply_preprocess(columns=columns, manager=self._dmanager)

    @Slot()
    def handle_regression(self):

        columns = self._select_cols.selection()
        self._graph.make_regression(data=self._dmanager.data, x=columns[0], y=columns[1])
        self._graph.setVisible(True)