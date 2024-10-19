import pandas as pd
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


"""

Module VirtualTable provides the class infrastructure and methods
to create a Virtual table that will remarcably increase the efficience 
and speed of displayin user's data sets into a table.

This is done by separating the data from the visualization.

"""

class VirtualTableModel(QAbstractTableModel):

    """
    This class is in charge of building a data model from a pandas 
    Data Frame, this model will provide the data for our Table View.
    It inherits the superclass QAbstractTableModel that allows to 
    manage data in a efficient way for GUI's.
    """

    def __init__(self, data=None):
        super().__init__()
        self._data = data if data is not None else pd.DataFrame()

    def rowCount(self, parent=QModelIndex()):
        #return the number of rows for our data frame
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        #return the number of columns of our dataFrame
        return len(self._data.columns) if not self._data.empty else 0
    
    def headerData(self, section, orientation, role):
        #seta header for out table
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:  # Encabezados de columnas
                return self._data.columns[section]  # Nombre de la columna
            elif orientation == Qt.Vertical:  # Encabezados de filas
                return str(section + 1)  # Numeración de filas (opcional)
        return None


    def data(self, index, role=Qt.DisplayRole):
        #return a cell value
        if role == Qt.DisplayRole and index.isValid():
            return str(self._data.iat[index.row(), index.column()])
        return None

    def setDataFrame(self, data):
        #allows to change the data frame
        self.beginResetModel()
        self._data = data
        self.endResetModel()

class VirtualTableView(QTableView):

    """
    This class is in charge of Visualazing a data model into the
    visible section of the table widget, as it inherits class QTableView
    that allows to deploy this feature.
    """
    def __init__(self, model: VirtualTableModel):
        super().__init__()
        #we provide the table viewer with our data model
        self.setModel(model)
        #we set a vertical scroll bar
        self.setVerticalScrollMode(QTableView.ScrollPerPixel)