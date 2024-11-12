from dataManagement.dataManager import DataManager

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QMessageBox,
    QButtonGroup
)

from PySide6.QtCore import Signal, Slot, Qt
import pandas as pd
import UserInterface.UIHelpers as helper

class PrepMenu(QWidget):

    preprocess_request = Signal()
    processed_data = Signal(pd.DataFrame)

    def __init__(self):

        super().__init__()
        self._manager = DataManager()

        # Declare layouts
        self._main_layout = QGridLayout()

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
        self._input_number.setVisible(False)
        self._apply_button = helper.create_button(text='Apply', event=self.on_apply_button)
        self._apply_button.setEnabled(False)


        # Connect signals
        self._constant_option.toggled.connect(self.toggle_input)

        # build layout
        self._main_layout.setHorizontalSpacing(10)
        self._main_layout.setVerticalSpacing(10)

        self._main_layout.addWidget(self._constant_option, 0, 0)  # Primera fila, primera columna
        self._main_layout.addWidget(self._input_number, 0, 1)  
        self._main_layout.addWidget(self._mean_option, 1, 0)
        self._main_layout.addWidget(self._median_option, 2, 0)
        self._main_layout.addWidget(self._remove_option, 3, 0)
        self._main_layout.addWidget(self._apply_button, 4, 1)

        self.setLayout(self._main_layout)
    

    @Slot(bool)
    def activate_menu(self, enabled: bool):

        self._constant_option.setEnabled(enabled)
        self._mean_option.setEnabled(enabled)
        self._median_option.setEnabled(enabled)
        self._remove_option.setEnabled(enabled)
        self._apply_button.setEnabled(enabled)
        self.toggle_input(checked=False)
        
        #Desseleccionar todos los botones
        self._preprocessing_opts.setExclusive(False)
    
        # Desmarcar todos los botones
        for button in self._preprocessing_opts.buttons():
            button.setChecked(False)
        
        # Volver a establecer el QButtonGroup como exclusivo
        self._preprocessing_opts.setExclusive(True)

    @Slot(bool)
    def toggle_input(self, checked: bool):

        """
        Enable and set visible the input field only if the 'Replace with a number' 
        option is selected.
        """

        self._input_number.setEnabled(checked)
        self._input_number.setVisible(checked)
        self._input_number.setText('')

    
    def on_apply_button(self):
        #emit request to handle preprocess
        self.preprocess_request.emit()


    def apply_preprocess(self, columns, manager: DataManager):

        choice = self._preprocessing_opts.checkedButton()
        
        try:

            if choice is self._remove_option:
                manager.delete(columns=columns)

            elif choice is self._mean_option:
                manager.replace(columns=columns)

            elif choice is self._median_option:
                manager.replace(columns=columns, value='median')
            
            elif choice is self._constant_option:
                constant_value = self._input_number.text()
                print(f"Constante introducida: {constant_value}")
                manager.replace(columns=columns, value = float(constant_value))

            self.processed_data.emit(manager.data)
            QMessageBox.information(self, "Succesfull preprocess", f"{columns[0]} and {columns[1]} no longer have null values")

        except Exception as e:
            helper.show_error_message(message=f"Preprocess could not be completed: {e}")