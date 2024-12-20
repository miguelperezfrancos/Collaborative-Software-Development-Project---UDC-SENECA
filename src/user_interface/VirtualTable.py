"""Module for creating efficient virtual tables for displaying data sets.

This module provides the class infrastructure and methods to create a Virtual
table that will remarkably increase the efficiency and speed of displaying
user's data sets. This is done by separating the data from the visualization.
"""

import pandas as pd
from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Slot


class VirtualTableModel(QAbstractTableModel):
    """Build a data model from a pandas DataFrame for Table View.

    This class is responsible for building a data model from a pandas
    DataFrame. This model will provide the data for our Table View.
    It inherits from QAbstractTableModel that allows efficient data
    management for GUIs.
    """

    def __init__(self, data=None):
        """Initialize the model with optional data.

        Args:
            data (pandas.DataFrame, optional): Initial data. Defaults to None.
        """
        super().__init__()
        self._data = data if data is not None else pd.DataFrame()

    def rowCount(self, parent=QModelIndex()):
        """Return the number of rows in the data frame.

        Args:
            parent (QModelIndex, optional): Parent index. Defaults to 
             QModelIndex().

        Returns:
            int: Number of rows.
        """
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        """Return the number of columns in the data frame.

        Args:
            parent (QModelIndex, optional): Parent index. Defaults to
              QModelIndex().

        Returns:
            int: Number of columns.
        """
        return len(self._data.columns) if not self._data.empty else 0

    def headerData(self, section, orientation, role):
        """Set header for the table.

        Args:
            section (int): Section index.
            orientation (Qt.Orientation): Header orientation.
            role (Qt.ItemDataRole): Data role.

        Returns:
            str: Header text or None.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def data(self, index, role=Qt.DisplayRole):
        """Return a cell value.

        Args:
            index (QModelIndex): Cell index.
            role (Qt.ItemDataRole, optional): Data role. Defaults to
              Qt.DisplayRole.

        Returns:
            str: Cell value or None.
        """
        if role == Qt.DisplayRole and index.isValid():
            return str(self._data.iat[index.row(), index.column()])
        return None

    def setDataFrame(self, data):
        """Update the data frame.

        Args:
            data (pandas.DataFrame): New data frame.
        """
        self.beginResetModel()
        self._data = data
        self.endResetModel()


class VirtualTableView(QTableView):
    """Visualize a data model in the table widget.

    This class is responsible for visualizing a data model in the
    visible section of the table widget. It inherits from QTableView
    to enable this feature.
    """

    def __init__(self, model: VirtualTableModel, 
                 min_column_width=100):
        """Initialize the table view with dynamic column sizing.

        Args:
            model (VirtualTableModel): Data model for the table.
            min_column_width (int): Minimum width for columns.
            max_column_width (int): Maximum width before horizontal scrolling.
        """
        super().__init__()
        self.setModel(model)
        self.setVerticalScrollMode(QTableView.ScrollPerPixel)
        
        # Configure horizontal header for interactive resizing
        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumSectionSize(min_column_width)
        horizontal_header.setStretchLastSection(False)
        
        # Store width parameters
        self._min_column_width = min_column_width
        
        # Connect to model reset to adjust columns initially
        model.modelReset.connect(self._adjust_columns)

    def _adjust_columns(self):
        """Dynamically adjust column widths based on content and width constraints."""
        for col in range(self.model().columnCount()):
            # Get current column width
            current_width = self.columnWidth(col)
            
            # Enforce minimum width
            if current_width < self._min_column_width:
                self.setColumnWidth(col, self._min_column_width)


    @Slot(pd.DataFrame)
    def set_data(self, data):
        """Update the table data.

        Args:
            data (pandas.DataFrame): New data to display.
        """
        self.model().setDataFrame(data)