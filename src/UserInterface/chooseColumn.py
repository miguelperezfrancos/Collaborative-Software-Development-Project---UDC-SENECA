from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox
)

from PySide6.QtCore import Signal, Slot
import pandas as pd

from UserInterface import Helpers as helper

class ChooseColumn(QWidget):

    send_selection = Signal(int) # señal para mandar la seleccion de un menú
    selected = Signal(bool) # señal para indicar que existe una seleccion válida
    make_regression = Signal() # señal para crear la regresión

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self._input_menu = helper.create_combo_box(default_item= "Select an input column", event=self.on_combo_box1_changed)
        self._output_menu = helper.create_combo_box(default_item="Select an output column", event=self.on_combo_box2_changed)
        self._create_model = helper.create_button(text="Generate model", event=self.on_create_model)
        self.selected.connect(self.enable_button)

        helper.set_layout(layout=layout, items= [
            self._input_menu,
            self._output_menu,
            self._create_model
        ])

        self.setLayout(layout)


    @Slot(pd.DataFrame)
    def update_selection(self, data):

        items = data.columns

        for menu in [self._input_menu, self._output_menu]:

            if menu == self._input_menu:
                default = 'Select an input column'
            else:
                default = 'Select an output column'

            menu.clear()
            menu.addItem(default)
            menu.addItems(items)


    def check_selection(self, menu):

        # Verificar si las selecciones son iguales
        if self._input_menu.currentText() == self._output_menu.currentText():

            QMessageBox.warning(self, "Error", "You cannot select the same column.")
            menu.setCurrentIndex(0)

        else:
            # Si no son iguales emitimos que la selcción es válida y las columnas seleccionadas
            self.selected.emit(True)

    def selection(self):

        """
        This function send column selection when
        preprocessing button is pressed
        """
        selection = [self._input_menu.currentText(), self._output_menu.currentText()]
        return selection


    def on_combo_box1_changed(self, index):

        if index != 0:  

            self.send_selection.emit(index-1)
            
            if self._output_menu.currentIndex() != 0:
                self.check_selection(menu=self._input_menu) # Revisar selección si se ha seleccionado una columna
        else :
            self.selected.emit(False) # Emitir False si se ha seleccionado la opción por defecto

    def on_combo_box2_changed(self, index):

        if index != 0:  

            self.send_selection.emit(index-1) #check NaN values
            
            if self._input_menu.currentIndex() != 0:
                self.check_selection(menu=self._output_menu) # revisar seleccion si se ha mandado una columna
        else:
            self.selected.emit(False) # emitir False si se ha seleccionado la opción por defecto


    @Slot(bool)
    def enable_button(self, enabled):
        self._create_model.setEnabled(enabled)

    def on_create_model(self):
        self.make_regression.emit()