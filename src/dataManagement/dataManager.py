import pandas as pd

class DataManager():

    def __init__(self, data=None):
        self._data = data

    """
    La interfaz gráfica debe detectar automáticamente las celdas con valores inexistentes (NaN o vacías) en las columnas seleccionadas para el modelo.

    El sistema debe alertar al usuario sobre la cantidad de valores inexistentes y en qué columnas se encuentran.
    """

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, ndata):
        if isinstance(ndata, pd.DataFrame):
            self._data = ndata
        else:
            raise ValueError('This should be a pandas data frame')
        
    def get_colums(self, index: int):
        """
        This funciton gets the columns where linear
        regression is going to be applied.
        """
        column = self._data.columns
        return column[index]
        
    def detect(self, column: str):
        """
        This function detects the rows with NaN values.
        """
        nan_sum = self._data[column].isna().sum()
        nan_indices = self._data[self._data[column].isna()].index

        print(nan_indices)
        print(nan_sum)
        

    def delete(self, column:str):
        """
        This function deletes the rows containing NaN values.
        """
        self._data.dropna(subset=column, inplace=True)
        return self._data 

    def replace(self, column: str, value = 'mean'):
        """
        This function replaces NaN values with a constant, mean our median values.
        """

        if value == 'mean':
            self._data.fillna({column: self._data.mean()}, inplace = True)

        elif value == 'median':
            self._data.fillna({column: self._data.median()}, inplace = True)

        elif isinstance(value, int) or isinstance(value, float):
            self._data.fillna({column: value}, inplace = True)
        
