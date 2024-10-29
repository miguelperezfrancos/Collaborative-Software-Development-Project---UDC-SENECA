from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QButtonGroup,
    QSpacerItem,
    QSizePolicy
)
import sys
import os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_root)
from PySide6.QtCore import Qt
from src.dataManagement.fileReader import FileReader
from src.dataManagement.dataManager import DataManager as dm
from src.dataManagement.linearRegression import Regression
import pandas as pd  
import src.UserInterface.widgetBuilder as builder


import matplotlib.pyplot as plt
from PySide6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class MainWindow(QWidget):
    
    """
    MainWindow class represents a graphical user interface (GUI) that allows
    users to interact with the application.
    """
    
    def __init__(self):

        """
        The constructor of the main window class. Here, widgets and layouts are created
        and set up.
        """
        
        super().__init__()

        self._dmanager = dm()

        # Store the selected columns
        self._input_column = None
        self._output_column = None

        #set window dimensions and name
        self.setWindowTitle("File Explorer")
        self.setGeometry(100, 100, 600, 400)

        #declare layouts
        self._main_layout = QVBoxLayout()
        self._hor_1 = QHBoxLayout()
        self._hor_2 = QHBoxLayout()

        self._vert_cc_lay = QVBoxLayout() # vertical layou for column choosing menu
        self._hor_choose_value = QHBoxLayout() # Horizontal Layout for choosing value
        self._vert_prep = QVBoxLayout() # vertical layout for choosing pre-processing method 

        #declare widgets
        self._file_indicator = builder.create_label(text="File path: ")
        self._path_label = builder.create_label(text="")
        self._open_file_button = builder.create_button(text="Open File Explorer", event=self.open_file_dialog)
        self._input_menu = builder.create_combo_box(default_item= "Select an input column", event=self.on_combo_box1_changed)
        self._output_menu = builder.create_combo_box(default_item="Select an output column", event=self.on_combo_box2_changed)
        self._confirm_cols_button = builder.create_button(text="Generate model", event=self.on_confirm_selection)
        self._table = builder.create_virtual_table()

        self._remove_option = builder.create_radio_button(text='Remove row')
        self._constant_option = builder.create_radio_button(text='Replace with a number')
        self._mean_option = builder.create_radio_button(text='Replace with mean')
        self._median_option = builder.create_radio_button(text='Replace with median')

        self._preprocessing_opts = QButtonGroup() # group radio buttons in the same 'button group', then add them
        self._preprocessing_opts.addButton(self._remove_option)
        self._preprocessing_opts.addButton(self._constant_option)
        self._preprocessing_opts.addButton(self._mean_option)
        self._preprocessing_opts.addButton(self._median_option)

        self._input_number = builder.create_text_box()
        self._apply_prep_button = builder.create_button(text='Apply', event=self.on_apply_button)
        self._apply_prep_button.setEnabled(False)

        #set up layouts
        self._set_layout(layout = self._hor_1, items=[self._file_indicator, self._path_label, self._open_file_button])
        self._set_layout(layout = self._vert_cc_lay, items=[self._input_menu, self._output_menu, self._confirm_cols_button]) # Vertical choose column layout
        self._set_layout(layout = self._hor_choose_value, items = [self._constant_option, self._input_number])
        self._set_layout(layout= self._vert_prep, items= [self._hor_choose_value, self._mean_option, self._median_option, self._remove_option,
                                                          self._apply_prep_button]) # Vertical layout with radio buttons
        self._set_layout(layout = self._hor_2, items = [self._vert_cc_lay, self._vert_prep])
        self._set_layout(layout = self._main_layout, items=[self._hor_1, self._table, self._hor_2])

        self._hor_choose_value.addItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        

        self.setLayout(self._main_layout)
        self._main_layout.setStretch(1, 10)  # Table expands
        self._main_layout.setStretch(2, 1)   # Combo box layout takes less space
        self.original_colors = {}

    def _set_layout(self, layout, items: list):

        """
        Automatically adds widget or layout to another layout.

        Parameters:
            layout: layout that will contain the widgets or another layouts.
            items (list): list of items that will be stored in the layout.
        """
        
        for i in items:
            if isinstance(i, QHBoxLayout) or isinstance(i, QVBoxLayout):
                layout.addLayout(i)
            else:
                layout.addWidget(i)

    def _show_error_message(self, message):
        """
        Displays an error message dialog.

        Parameters:
            message (str): The error message to display.
        """
        QMessageBox.critical(self, "Error", message, QMessageBox.Ok)

    def _load_file(self, file_path):

        """
        Loads the content of the file at the given path into the table widget.
        Handles different file formats (e.g., CSV, Excel, SQLite) and errors
        such as unsupported formats, empty files, or parsing issues.

        It also sends file to the data manager class and stablishe the data as
        the current model for the virtual table.

        Parameters:
            file_path (str): The path to the file to be loaded.
        """

        reader = FileReader()
        try:
            df = reader.parse_file(file_path)
            # 'send' the dataFrame to the data manager
            self._dmanager.data = df
            self._table.model().setDataFrame(df)

        except:  # Catch any other unknown errors
            self._show_error_message('ERROR: Unknown error')    


        # Update regression entry menu
        self._change_column_selection(menu=self._input_menu, items=df.columns,
                                      default_msg='Select an input column')
        
        self._change_column_selection(menu=self._output_menu, items=df.columns, 
                                      default_msg='Select an output column')

        # Reset previously selected columns
        self.input_column = None
        self.output_column = None

    def _change_column_selection(self, menu: QComboBox, items, default_msg: str):

        """
        This funtion updates a QComboBox item list (when different data is loaded to the app).

        Parameters:
            menu (QComboBox): menu that will be updated.
            items: new items thath will be added to the menu.
            default_msg (str): default option for the menu
        """

        menu.clear()
        menu.addItem(default_msg)
        menu.addItems(items)


    def _raise_nan_message(self, col_name: str):

        """
        This function checks if a column of the data frame has NaN values, if it does,
        it will inform the user about it raising an informative message.

        Parameters:
            col_name: name o fthe column in the data frame.
        """

        num_nan = self._dmanager.detect(column=col_name)

        if num_nan > 0:
            QMessageBox.information(self, "Unknown Values", f'{col_name} has {num_nan} unknown values, you might want to pre-process your data.')


    def open_file_dialog(self):

        """
        This function defines the events that will take place
        if user clicks Open File button.
        """

        #Gestión de errores: el archivo no se puede abrir o está corrupto

        # File dialog settings
        options = QFileDialog.Options()
        allowed_extensions = "Compatible files (*.csv *.xlsx *.xls *.sqlite *.db)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File: ", "", allowed_extensions, options=options)

        # If a file is selected, load it into the table
        if file_path:

            try:
                self._load_file(file_path)
                self._path_label.setText(f"{file_path}")
            except:
                pass
            
    def on_combo_box1_changed(self, index):

        if index > 0:  # Ensure valid input column is selected
            col_index = index - 1
            col_name = self._dmanager.get_colums(index=col_index)

            # Check if column is the same as combo_box2
            if col_name == self._output_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self._input_menu.setCurrentIndex(0)  # Reset combo_box1 selection
            else:
                self._input_column = col_name
                self._raise_nan_message(col_name=self._input_column)

        else:
            self._input_column = None
        
        self._change_widget_status(layout = self._vert_prep)


    def on_combo_box2_changed(self, index):

        """
        This column acts as 
        """

        if index > 0:  # Ensure valid output column is selected

            col_index = index - 1
            col_name = self._dmanager.get_colums(index=col_index)

            # Check if column is the same as combo_box1
            if col_name == self._input_column:
                QMessageBox.warning(self, "Error", "You cannot select the same column.")
                self._output_menu.setCurrentIndex(0)  # Reset combo_box2 selection
            else:
                self._output_column = col_name
                self._raise_nan_message(col_name=self._output_column)
        else:
            self._output_column = None
            
        self._change_widget_status(layout= self._vert_prep)

    def on_confirm_selection(self):

        """
        This function acts as the event for pressing confirm selection button (choosing input and output)
        values for linear regression model.
        """

        # Inform user about his choice
        if self._input_column is not None and self._output_column is not None:
            QMessageBox.information(self, "Selection Confirmed", f"Input Column: {self._input_column}, Output Column: {self._output_column}")
        # Request user to choose two differetn columns 
        else:
            QMessageBox.warning(self, "Selection Error", "Please select two different columns before confirming.")

    def on_apply_button(self):

        """
        This function is the 'event' that takes place when the user apply changes
        on preprocessing option.
        """

        choice = self._preprocessing_opts.checkedButton()
        columns = [self._input_column, self._output_column]
        print(columns)

        if len(columns) > 0:

            try:

                if choice is self._remove_option:
                    self._dmanager.delete(columns=columns)
                elif choice is self._constant_option:

                    constant_value = self._input_number.text()
                    print(f"Constante introducida: {constant_value}")
                    self._dmanager.replace(columns=columns, value = float(constant_value))
                
                elif choice is self._mean_option:
                    self._dmanager.replace(columns=columns)
                elif choice is self._median_option:
                    self._dmanager.replace(columns=columns, value='median')

                # Reset table model to processed data
                self._table.model().setDataFrame(self._dmanager.data)
                QMessageBox.information(self, "Succesfull preprocess", f"{self._input_column} and {self._output_column} no longer have null values")

            except:
                self._show_error_message("ERROR: pre-process could not be completed")



    def _change_widget_status(self, layout):

        """
        This function activates pre-processing menu when both input and output are selected,
        if not, menu will be deactivated.
        """

        if self._input_column is not None and self._output_column is not None:
            enabled = True
        else:
            enabled = False

        # Iterar sobre todos los widgets del layout
        for i in range(layout.count()):
            item = layout.itemAt(i)

            # Si el item es un widget, lo activamos/desactivamos
            widget = item.widget()
            if widget:
                widget.setEnabled(enabled)

            # Si el item es un layout, llamamos recursivamente
            inner_layout = item.layout()
            if inner_layout:
                self._change_widget_status(inner_layout)


    def perform_linear_regression(self):
        if self._input_column is None or self._output_column is None:
            self._show_error_message("Please select input and output columns first.")
            return

        regression = Regression()
        regression.make_model(self._dmanager.data, self._input_column, self._output_column)

        r2 = regression.get_r_squared()
        mse = regression.get_MSE()
        model_line = regression.get_regression_line()

        # Create a new widget to display the plot
        plot_widget = QWidget()
        plot_layout = QVBoxLayout()
        plot_widget.setLayout(plot_layout)

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(self._dmanager.data[self._input_column], self._dmanager.data[self._output_column], color='blue', alpha=0.5)
        ax.plot(self._dmanager.data[self._input_column], regression._pred_line, color='red')
        ax.set_xlabel(self._input_column)
        ax.set_ylabel(self._output_column)
        ax.set_title('Linear Regression')

        # Add text with model information
        text = f"Model: {model_line}\nR² = {r2:.4f}\nMSE = {mse:.4f}"
        ax.text(0.05, 0.95, text, transform=ax.transAxes, verticalalignment='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

        # Create a canvas for the plot and add it to the layout
        canvas = FigureCanvas(fig)
        plot_layout.addWidget(canvas)

        # Add the plot widget to the main layout
        self._main_layout.addWidget(plot_widget)





    def on_confirm_selection(self):
        """
        This function acts as the event for pressing the confirm selection button (choosing input and output)
        values for linear regression model.
        """
        if self._input_column is not None and self._output_column is not None:
            try:
                regression = Regression()
                regression.make_model(self._dmanager.data, self._input_column, self._output_column)

                r2 = regression.get_r_squared()
                mse = regression.get_MSE()
                model_line = regression.get_regression_line()

                # Create a new widget to display the plot
                plot_widget = QWidget()
                plot_layout = QVBoxLayout()
                plot_widget.setLayout(plot_layout)

                # Create the plot
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(self._dmanager.data[self._input_column], self._dmanager.data[self._output_column], color='blue', alpha=0.5)
                ax.plot(self._dmanager.data[self._input_column], regression._pred_line, color='red')
                ax.set_xlabel(self._input_column)
                ax.set_ylabel(self._output_column)
                ax.set_title('Linear Regression')

                # Add text with model information
                text = f"Model: {model_line}\nR² = {r2:.4f}\nMSE = {mse:.4f}"
                ax.text(0.05, 0.95, text, transform=ax.transAxes, verticalalignment='top', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

                # Create a canvas for the plot and add it to the layout
                canvas = FigureCanvas(fig)
                plot_layout.addWidget(canvas)

                # Remove any existing plot widget
                for i in reversed(range(self._main_layout.count())): 
                    widget = self._main_layout.itemAt(i).widget()
                    if isinstance(widget, QWidget) and widget != self:
                        widget.setParent(None)

                # Add the plot widget to the main layout
                self._main_layout.addWidget(plot_widget)

                QMessageBox.information(self, "Model Generated", f"Linear regression model has been generated and plotted.")
            except Exception as e:
                self._show_error_message(f"Error generating model: {str(e)}")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select two different columns before confirming.")