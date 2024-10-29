from dataManagement.dataManager import DataManager

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QButtonGroup
)

from PySide6.QtCore import Signal, Slot

import UserInterface.UIHelpers as helper

class Prepmenu(QWidget):

    def __init__(self):

        super.__init__()
        self._manager = DataManager()

        self._container = QWidget()

        # Declare layouts
        self._main_layout = QVBoxLayout()
        self._constant_layout = QHBoxLayout()

        self._remove_option = helper.create_radio_button(text='Remove row')
        self._constant_option = helper.create_radio_button(text='Replace with a number')
        self._mean_option = helper.create_radio_button(text='Replace with mean')
        self._median_option = helper.create_radio_button(text='Replace with median')

        self._preprocessing_opts = QButtonGroup() # group radio buttons in the same 'button group', then add them
        self._preprocessing_opts.addButton(self._remove_option)
        self._preprocessing_opts.addButton(self._constant_option)
        self._preprocessing_opts.addButton(self._mean_option)
        self._preprocessing_opts.addButton(self._median_option)

        self._input_number = helper.create_text_box()
        self._apply_button = helper.create_button(text='Apply', event=self.on_apply_button)
        self._apply_button.setEnabled(False)

        # build layouts
        helper.set_layout(layout=self._constant_layout, items = [self._constant_option, self._input_number])
        helper.set_layout(layout=self._main_layout, items= [
            self._constant_layout,
            self._mean_option,
            self._median_option,
            self._remove_option,
            self._apply_button
        ])
    
    
    @Slot(bool)
    def activate_menu(self, enabled: bool):

        layout = self._main_layout

        for i in range(layout.count()):

            item = layout.itemAt(i)

            # Si el item es un widget, lo activamos/desactivamos
            widget = item.widget()
            if widget:
                widget.setEnabled(enabled)

            # Si el item es un layout, llamamos recursivamente
            inner_layout = item.layout()
            if inner_layout:
                self.activate_menu(inner_layout)
        

    
    def on_apply_button(self):
        pass





