"""
Main window implementation for the Linear Regression application.

This module provides the main window interface for a linear regression 
analysis tool.

It allows users to:
    - Load and visualize data
    - Select columns for analysis
    - Preprocess data (handle missing values, etc.)
    - Generate and visualize regression models
    - Make predictions using the generated models
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Slot, Signal
import pandas as pd

from src.data_management import DataManager, Model
from src.user_interface import (
    ChooseColumn,
    ChooseFile,
    PrepMenu,
    RegressionGraph,
    RepModel,
)
import src.user_interface.ui_helpers as helper
from src.user_interface.predictions import Predict


class MainWindow(QMainWindow):
    """
    Main window class that handles the application's UI and functionality.

    This class serves as the primary container for all UI components and manages
    the interaction between different parts of the application. It coordinates
    data loading, preprocessing, model generation, and visualization.

    Attributes:
        scroll_area (QScrollArea): Main scrollable container for all widgets
        _data_manager (DataManager): Handles all data operations
        _main_layout (QVBoxLayout): Primary vertical layout for the window
        _content_widget (QWidget): Container widget for the main layout
    """

    is_model = Signal(Model)
    do_preprocess = Signal(bool)

    def __init__(self):
        """
        Initialize the main window and set up the UI components.

        Sets up the window properties, creates and arranges all UI components,
        establishes signal-slot connections, and configures the initial state
        of the application.
        """
        super().__init__()

        self.setWindowTitle('TrendLine')
        self.setGeometry(100, 100, 1000, 550)

        self._data_manager = DataManager()
        self._model = Model()

        # Set up main layout and content widget
        self._main_layout = QVBoxLayout()
        self._content_widget = QWidget()
        self._content_widget.setLayout(self._main_layout)
        self._content_widget.setObjectName("content_widget")

        # Set up scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self._content_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        # Initialize UI components
        self._init_ui_components()
        self._setup_layouts()
        self._setup_connections()

        # Set the scroll area as the central widget
        self.setCentralWidget(self.scroll_area)
        self._content_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # Set window layout
        self.setLayout(self._main_layout)

    def _init_ui_components(self):
        """
        Initialize all UI components of the application.

        Creates and configures the following components:
            - File chooser menu
            - Data table viewer
            - Column selector
            - Preprocessing menu
            - Regression graph
            - Model information display
            - Prediction interface

        Also sets initial visibility states and size constraints for components.
        """
        self._choose_file_menu = ChooseFile()
        self._table = helper.create_virtual_table()
        self._select_cols = ChooseColumn()
        self._preprocess = PrepMenu()
        self._graph = RegressionGraph()
        self._model_info = RepModel()
        self._predict = Predict()

        # Set initial visibility
        self._model_info.setVisible(False)
        self._graph.setVisible(False)

        # Set size constraints
        self._table.setMinimumHeight(250)
        self._graph.setMinimumHeight(450)

    def _setup_layouts(self):
        """
        Set up all layouts for the UI components.

        Organizes the UI components into a hierarchical layout structure:
            - Main vertical layout containing all other layouts
            - Processing options in horizontal layout
            - Model visualization and information in combined layouts
            - Button layout for model generation
        
        Each layout is configured with appropriate spacing and alignment
        to create a user-friendly interface.
        """
        # Processing options layout
        self._cp_layout = QHBoxLayout()
        helper.set_layout(
            layout=self._cp_layout,
            items=[self._select_cols, self._preprocess]
        )

        # Model representation layouts
        self._model_h_layout = QHBoxLayout()
        self._model_v_layout = QVBoxLayout()
        helper.set_layout(
            layout=self._model_v_layout,
            items=[self._model_info, self._predict]
        )

        self._model_two_layout = QHBoxLayout()
        helper.set_layout(
            layout=self._model_two_layout,
            items=[self._graph, self._model_v_layout, self._model_h_layout]
        )

        # Create model button layout
        self._gen_button_layout = QHBoxLayout()
        self._gen_button_layout.addWidget(self._select_cols.create_model)
        self._gen_button_layout.setAlignment(Qt.AlignCenter)

        # Add components to main layout
        self._main_layout.addWidget(self._choose_file_menu)
        self._main_layout.addWidget(self._table)
        self._main_layout.addLayout(self._cp_layout)
        self._main_layout.addLayout(self._gen_button_layout)
        self._main_layout.addLayout(self._model_two_layout)

    def _setup_connections(self):
        """
        Set up all signal-slot connections between UI components.

        Establishes connections for:
            - File loading and data display
            - Column selection and validation
            - Preprocessing triggers and updates
            - Model generation and visualization
            - Prediction updates

        These connections enable the interactive functionality of the 
        application, allowing components to communicate and respond to user 
        actions.
        """
        # File menu connections
        self._choose_file_menu.file_selected.connect(self.get_data)
        self._choose_file_menu.file_selected.connect(self._table.set_data)
        self._choose_file_menu.file_selected.connect(
            self._select_cols.update_selection
        )
        self._choose_file_menu.hide_show.connect(self.hide_show_data)

        # Column selection connections
        self._select_cols.send_selection.connect(self.show_nan_values)
        self._select_cols.selected.connect(self.activate_preprocess)

        # Preprocessing connections
        self._preprocess.preprocess_request.connect(self.handle_preprocess)
        self._preprocess.processed_data.connect(self._table.set_data)

        # Model info connections
        self.is_model.connect(self._graph.make_graph)
        self.is_model.connect(self._model_info._update_model)
        self._choose_file_menu.loaded_model.connect(
            self._model_info._update_model
        )

        # Prediction connections
        self.is_model.connect(self._predict.update_model)
        self._choose_file_menu.loaded_model.connect(
            self._predict.update_model
        )

        # Regression connection
        self._select_cols.make_regression.connect(self.handle_regression)

    @Slot(pd.DataFrame)
    def get_data(self, data):
        """
        Store the input data in the data manager.

        Args:
            data (pd.DataFrame): The DataFrame containing the loaded data
                               from the user's file selection.
        """
        self._data_manager.data = data

    @Slot(int)
    def show_nan_values(self, index):
        """
        Display a message box showing the number of NaN values in a selected 
        column.

        Args:
            index (int): The index of the selected column in the DataFrame.

        This method helps users identify data quality issues before proceeding
        with the analysis, prompting them to consider preprocessing steps
        if necessary.
        """
        col_name = self._data_manager.data.columns[index]
        num_nan = self._data_manager.detect(column=col_name)

        if num_nan > 0:
            QMessageBox.information(
                self,
                "Unknown Values",
                f'{col_name} has {num_nan} unknown values, '
                'you might want to pre-process your data.'
            )

    @Slot(bool)
    def activate_preprocess(self, selected):

        if selected:

            columns = self._select_cols.selection()
            nan = 0

            for c in columns:
                if c in self._data_manager.data.columns:
                    nan += self._data_manager.detect(c)

            if nan > 0:
                self._preprocess.activate_menu(True)
            else:
                self._preprocess.activate_menu(False)

        else:
            self._preprocess.activate_menu(False)

    @Slot()
    def handle_preprocess(self):
        """
        Handle preprocessing request from the user.

        Retrieves the selected columns and passes them to the preprocessing
        module along with the data manager. This enables the preprocessing
        of specific columns while maintaining the integrity of the entire
        dataset.
        """
        columns = self._select_cols.selection()
        self._preprocess.apply_preprocess(
            columns=columns,
            manager=self._data_manager
        )

    @Slot()
    def handle_regression(self):
        """
        Handle the regression model generation request.

        This method:
            1. Checks for NaN values in the selected columns
            2. Attempts to generate the regression model if data is clean
            3. Updates the visualization components
            4. Handles any errors that occur during model generation
        
        If NaN values are found, prompts the user to preprocess the data first.
        """
        columns = self._select_cols.selection()

        num_nan = sum(
            self._data_manager.detect(column)
            for column in columns[:2]
        )

        if num_nan == 0:
            try:
                self._model.create_from_data(
                    data=self._data_manager.data,
                    input_col=columns[0],
                    output_col=columns[1]
                )
                self.is_model.emit(self._model)
                self._show_model_components(True)
            except Exception as e:
                helper.show_error_message(f'unexpected error: {e}')
                if not self._graph.isVisible():
                    self._show_model_components(False)
        else:
            helper.show_error_message(
                'Data contains NaN values: please, apply preprocess '
                'before generating model.'
            )

    def _show_model_components(self, show: bool):
        """
        Show or hide model-related components.

        Args:
            show (bool): If True, displays the model components;
                        if False, hides them.

        Controls the visibility of:
            - Regression graph
            - Model information panel
            - Prediction interface
        """
        self._graph.setVisible(show)
        self._model_info.setVisible(show)
        self._predict.setVisible(show)

    @Slot(bool)
    def hide_show_data(self, show: bool):
        """
        Show or hide widgets based on the loaded file type.

        Args:
            show (bool): If True, shows data-related widgets and hides model;
                        if False, shows model-related widgets and hides data.

        This method manages the UI state transitions between:
            - Data viewing/preprocessing mode
            - Model visualization/prediction mode

        It handles both the reorganization of layouts and the visibility
        of individual components to create a coherent user experience.
        """
        old_layout = self._model_h_layout if show else self._model_v_layout
        new_layout = self._model_v_layout if show else self._model_h_layout

        # Move widgets between layouts
        old_layout.removeWidget(self._model_info)
        old_layout.removeWidget(self._predict)
        new_layout.addWidget(self._model_info)
        new_layout.addWidget(self._predict)

        # Update widget visibility
        self._table.setVisible(show)
        self._select_cols.setVisible(show)
        self._preprocess.setVisible(show)
        self._preprocess.toggle_input(checked=False)
        self._select_cols.create_model.setVisible(show)
        self._graph.setVisible(False)
        self._model_info.setVisible(not show)
        self._predict.setVisible(not show)