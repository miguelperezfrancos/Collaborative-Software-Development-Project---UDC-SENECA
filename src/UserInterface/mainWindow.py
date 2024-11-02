from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,
)
from PySide6.QtCore import Qt, Signal, Slot
import pandas as pd
from UserInterface import ChooseColumn, ChooseFile, PrepMenu, RegressionGraph
from UserInterface.changeNumberWidget import ChangeNumberWidget  # Importar el nuevo widget
import UserInterface.UIHelpers as helper
from dataManagement.dataManager import DataManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Rafa es gay. Encima es de oleiros.')
        self.setGeometry(100, 100, 1000, 500)

        self._dmanager = DataManager()

        # Crear un QScrollArea
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)  # Hacer que el contenido se ajuste automáticamente

        # Crear el layout principal
        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)

        # Crear un contenedor para los botones y el textbox
        self._button_container = QWidget()
        self._button_layout = QHBoxLayout()

        

    

        # Agregar el contenedor de botones al layout principal
        self._main_layout.addWidget(self._button_container)

        # Crear otros widgets
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()  # Suponiendo que esta función devuelve un QWidget
        self._table.setMinimumHeight(250)
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()

        # Crear el gráfico
        self._graph = RegressionGraph()  # Suponiendo que esta función devuelve un QWidget
        self._graph.setMinimumHeight(400)

        # Agregar widgets al layout principal
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addWidget(self._button_container)  # Agregar contenedor de botones
        self._main_layout.addWidget(self._select_cols)
        self._main_layout.addWidget(self._preprocess)

        # Configuración del área de scroll para el gráfico
        self._graph_scroll_area = QScrollArea()
        self._graph_scroll_area.setFixedHeight(500)  # Ajusta a la altura deseada
        self._graph_scroll_area.setWidgetResizable(True)
        self._graph_scroll_container = QWidget()
        self._graph_scroll_layout = QVBoxLayout()
        self._graph_scroll_layout.addWidget(self._graph)
        self._graph_scroll_container.setLayout(self._graph_scroll_layout)
        self._graph_scroll_area.setWidget(self._graph_scroll_container)

        # Agregar el área de scroll del gráfico al layout principal
        self._main_layout.addWidget(self._graph_scroll_area)

        # Establecer el widget de contenido en el área de desplazamiento
        self._scroll_area.setWidget(self._content_widget)

        # Establecer el área de scroll como el widget central
        self.setCentralWidget(self._scroll_area)

        # connect signals and slots
        self._choose_file_menu.file_selected.connect(self.get_data)  # send selected file to data manager
        self._choose_file_menu.file_selected.connect(self._table.set_data)  # send data to table
        self._choose_file_menu.file_selected.connect(self._select_cols.update_selection)  # send data to column selection menu

        self._select_cols.send_selection.connect(self.show_nan_values)  # get selected column to check if it has NaN values
        self._select_cols.selected.connect(self._preprocess.activate_menu)  # send selection status to activate preprocess menu

        self._preprocess.preprocess_request.connect(self.handle_preprocess)  # handle preprocessing
        self._preprocess.processed_data.connect(self._table.set_data)  # update table content when preprocess is done

        self._select_cols.make_regression.connect(self.handle_regression)  # establish connection to create regression graph

    def handle_number_change(self, number):
        """ Manejar el cambio de número. """
        if number is not None:
            print(f"Número cambiado a: {number}")  # Aquí puedes manejar el número como desees
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce un número válido.")

    @Slot(pd.DataFrame)
    def get_data(self, data):
        self._dmanager.data = data

    @Slot(int)
    def show_nan_values(self, index):
        """
        This function checks if a column of the data frame has NaN values, if it does,
        it will inform the user about it raising an informative message.
        """
        col_name = self._dmanager.data.columns[index]
        num_nan = self._dmanager.detect(column=col_name)

        if num_nan > 0:
            QMessageBox.information(self, "Unknown Values", f'{col_name} has {num_nan} unknown values, you might want to pre-process your data.')

    @Slot()
    def handle_preprocess(self):
        """
        This function calls the data preprocessing method
        when the apply preprocess button is pressed (this
        emits a signal).
        """
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
        self._graph_scroll_area.setFixedHeight(500)
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

