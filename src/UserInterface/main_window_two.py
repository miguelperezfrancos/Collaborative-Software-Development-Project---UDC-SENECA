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


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('Rodri es gay')
        self.setGeometry(100, 100, 1000, 500)

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


        # connect dignals and slots
        self._choose_file_menu.file_selected.connect(self._table.set_data)
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)
        self._select_cols.selected.connect(self._preprocess.activate_menu)
       