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

class PrepMenu(QWidget):

    def __init__(self):

        super().__init__()
        self._manager = DataManager()

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

        # set container
        self.setLayout(self._main_layout)
    

    @Slot(bool)
    def activate_menu(self, enabled: bool):

        self._constant_option.setEnabled(enabled)
        self._mean_option.setEnabled(enabled)
        self._median_option.setEnabled(enabled)
        self._remove_option.setEnabled(enabled)
        self._apply_button.setEnabled(enabled)

    
    def on_apply_button(self):
        pass