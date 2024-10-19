import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

class VirtualTableModel(QAbstractTableModel):
    def __init__(self, dataframe=None):
        super().__init__()
        self.dataframe = dataframe if dataframe is not None else pd.DataFrame()

    def rowCount(self, parent=QModelIndex()):
        return len(self.dataframe)

    def columnCount(self, parent=QModelIndex()):
        return len(self.dataframe.columns) if not self.dataframe.empty else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            return str(self.dataframe.iat[index.row(), index.column()])
        return None

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self.dataframe = dataframe
        self.endResetModel()

class VirtualTableView(QTableView):
    def __init__(self, model):
        super().__init__()
        self.setModel(model)
        self.setVerticalScrollMode(QTableView.ScrollPerPixel)