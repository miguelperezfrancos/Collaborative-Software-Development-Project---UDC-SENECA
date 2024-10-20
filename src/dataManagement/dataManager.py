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
        This function detects the number of rows with NaN values.
        """
        
        nan_sum = self._data[column].isna().sum()

        print(nan_sum)
        return nan_sum


    def delete(self, columns:list):
        """
        This function deletes the rows containing NaN values.
        """
        new_df = self._data.dropna(subset=columns)
        new_df.reset_index(drop=True, inplace=True)
        self._data = new_df
        return self._data

    def replace(self, columns: list, value = 'mean'):
        """
        This function replaces NaN values with a constant, mean our median values.
        """
        nan_cols = [c for c in columns if self.detect(c) > 0]

        if value == 'mean':
            nan_values = [self._data[c].mean() for c in nan_cols]
            
        elif value == 'median':
            nan_values = [self._data[c].median() for c in nan_cols]

        elif isinstance(value, int) or isinstance(value, float):
            nan_values = [value for _ in nan_cols]


        c_v_dict = dict(zip(nan_cols, nan_values))
        self._data.fillna(c_v_dict, inplace = True)


