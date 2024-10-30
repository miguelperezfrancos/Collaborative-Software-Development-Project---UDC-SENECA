from PySide6.QtWidgets import( 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout    
)

from UserInterface.openFile import ChooseFile
from UserInterface.VirtualTable import VirtualTableModel, VirtualTableView
import UserInterface.UIHelpers as helper
from UserInterface.chooseColumn import ChooseColumn
from UserInterface.prepMenu import PrepMenu
from PySide6.QtCore import Signal, Slot
import pandas as pd
from dataManagement.dataManager import DataManager


class MainWindow(QMainWindow):

    preprocess_settings = Signal(dict)

    def __init__(self):

        super().__init__()

        self.setWindowTitle('Rodri es gay')
        self.setGeometry(100, 100, 1000, 500)

        self._dmanager = DataManager()

        #create main container
        self._container = QWidget()

        #create layout
        self._main_layout = QVBoxLayout()

        # create file choosing menu
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()

        self._cp_layout = QHBoxLayout()

        helper.set_layout(layout=self._cp_layout, items = [
            self._select_cols,
            self._preprocess
        ])

        helper.set_layout(layout=self._main_layout, items = [
            self._choose_file_menu,
            self._table,
            self._cp_layout
        ])

        self._container.setLayout(self._main_layout)
        self.setCentralWidget(self._container)
        self._main_layout.setStretch(1, 10)  # Table expands
        self._main_layout.setStretch(2, 1)   # Combo box layout takes less space


        # connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data) # poner los datos en el data manager
        self._choose_file_menu.file_selected.connect(self._table.set_data) # se envían los datos a la tabla
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection) # se envian los datos al menu de seleccion de columnas
        self._select_cols.selected.connect(self._preprocess.activate_menu) # se envía la señal de activarse al menu del preprocesado
        self._preprocess.preprocess_request.connect(self.handle_preprocess) 
        self._preprocess.processed_data.connect(self._table.set_data) #añadir los datos preprocesados a la tabla


    @Slot(pd.DataFrame)
    def get_data(self, data):
        self._dmanager.data = data

    @Slot()
    def handle_preprocess(self):

        """
        Esta function llama al método de preprocesado de datos
        cuando el botón de apply preprocess es presionado (este
        emite una señal)
        """

        columns = self._select_cols.selection()
        self._preprocess.apply_preprocess(columns=columns, manager=self._dmanager)