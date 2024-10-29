from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QMessageBox
)

from PySide6.QtCore import Signal, Slot
import pandas as pd

import UserInterface.widgetBuilder as builder


class ChooseColumn(QWidget):

    send_selection = Signal(list) # señal para mandar la seleccion actual de columnas
    selected = Signal(bool) # señal para indicar que existe una seleccion válida

    def __init__(self):

        super.__init__()

        self._input_menu = builder.create_combo_box(default_item= "Select an input column", event=self.on_combo_box1_changed)
        self._output_menu = builder.create_combo_box(default_item="Select an output column", event=self.on_combo_box2_changed)
        self._create_model = builder.create_button(text="Generate model", event=self.on_create_model)


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


    def check_selection(self):

        # Verificar si las selecciones son iguales
        if self._input_menu.currentText() == self._output_menu.currentText():

            QMessageBox.warning(self, "Error", "You cannot select the same column.")

        else:

            # Si no son iguales emitimos que la selcción es válida y las columnas seleccionadas

            selection = [self._input_menu.currentText(), self._output_menu.currentText()]
            self.send_selection.emit(selection)
            self.selected.emit(True)


    def on_combo_box1_changed(self, index):

        if index is not 0:
            self.check_selection() # Revisar selección si se ha seleccionado una columna
        else:
            self.selected.emit(False) # Emitir False si se ha seleccionado la opción por defecto

    def on_combo_box2_changed(self, index):

        if index is not 0:
            self.check_selection() # revisar seleccion si se ha mandado una columna
        else:
            self.selected.emit(False) # emitir False si se ha seleccionado la opción por defecto

    def on_create_model(self):
        pass


