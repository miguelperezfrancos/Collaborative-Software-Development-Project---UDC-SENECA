from PySide6.QtWidgets import ( 
    QMainWindow, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,    
    QSizePolicy,
)

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
import pandas as pd
from dataManagement.dataManager import DataManager

from UserInterface import (ChooseColumn, 
                           ChooseFile, 
                           PrepMenu, 
                           RegressionGraph)

import UserInterface.UIHelpers as helper


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Rafa es gay. Encima es de oleiros.')
        self.setGeometry(100, 100, 1000, 500)

        self._dmanager = DataManager()

        # Crear el layout principal
        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)

        # Crear un área de scroll principal
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidget(self._content_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Desactivar el scroll horizontal
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Crear otros widgets
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()  # Suponiendo que esta función devuelve un QWidget
        self._table.setMinimumHeight(250)
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()

        # Crear el gráfico
        self._graph = RegressionGraph()  # Suponiendo que esta función devuelve un QWidget
        self._graph.setMinimumHeight(350)

        # Configuración del área de scroll para el gráfico
        self._graph_scroll_area = QScrollArea()
        self._graph_scroll_area.setWidgetResizable(True)
        self._graph_scroll_container = QWidget()
        self._graph_scroll_layout = QVBoxLayout()
        self._graph_scroll_layout.addWidget(self._graph)
        self._graph_scroll_container.setLayout(self._graph_scroll_layout)
        self._graph_scroll_area.setWidget(self._graph_scroll_container)

        # Layout de opciones de procesamiento
        self._cp_layout = QHBoxLayout()
        helper.set_layout(layout=self._cp_layout, items=[self._select_cols, self._preprocess])

        # Agregar widgets al layout principal
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addLayout(self._cp_layout)
        self._main_layout.addWidget(self._graph_scroll_area)  # Añadido scroll específico para la gráfica

        # Establecer el área de scroll como el widget central
        self.setCentralWidget(self._scroll_area)
        self._content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #
        self.setLayout(self._main_layout)

        # connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data)  # send selected file to data manager
        self._choose_file_menu.file_selected.connect(self._table.set_data)  # send data to table
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)  # send data to column selection menu

        self._select_cols.send_selection.connect(self.show_nan_values)  # get selected column to check if it has NaN values
        self._select_cols.selected.connect(self._preprocess.activate_menu)  # send selection status to activate preprocess menu

        self._preprocess.preprocess_request.connect(self.handle_preprocess)  # handle preprocessing
        self._preprocess.processed_data.connect(self._table.set_data)  # update table content when preprocess is done

        self._select_cols.make_regression.connect(self.handle_regression)  # establish connection to create regression graph

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
        
        # Reiniciar el gráfico
        if hasattr(self, '_graph'):
            self._main_layout.removeWidget(self._graph_scroll_area)
            self._graph_scroll_area.deleteLater()  # Eliminar el área de scroll anterior
        
        # Crear nuevo gráfico
        self._graph = RegressionGraph()  # Suponiendo que esta función devuelve un QWidget
        self._graph.setMinimumHeight(350)
    
        # Configuración del área de scroll para el gráfico
        self._graph_scroll_area = QScrollArea()
        self._graph_scroll_area.setWidgetResizable(True)
        self._graph_scroll_container = QWidget()
        self._graph_scroll_layout = QVBoxLayout()
        self._graph_scroll_layout.addWidget(self._graph)
        self._graph_scroll_container.setLayout(self._graph_scroll_layout)
        self._graph_scroll_area.setWidget(self._graph_scroll_container)
    
        # Añadir el nuevo gráfico al layout
        self._main_layout.addWidget(self._graph_scroll_area)
    
        # Generar la regresión
        self._graph.make_regression(data=self._dmanager.data, x=columns[0], y=columns[1])
        self._graph.setVisible(True)
    
        # Actualizar el layout
        self._main_layout.update()
        self._main_layout.activate()
    
