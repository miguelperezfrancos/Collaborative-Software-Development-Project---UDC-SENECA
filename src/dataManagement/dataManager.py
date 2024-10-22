import pandas as pd

class DataManager():

    """
    This class will be used to implement methods and variables needed by the application
    for operating with data loaded by user in the application. It also keeps track of the 
    data model shown on the interface.
    """

    def __init__(self, data=None):
        self._data = data

   
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, ndata):
        if isinstance(ndata, pd.DataFrame):
            self._data = ndata
        else:
            raise ValueError('This should be a pandas data frame')
        
    def get_colums(self, index: int) -> str:

        """
        This funciton gets the name of a column base on 
        an index.

        Parameters:
            index (int)

        Returns: 
            column[index] (str): name of the corresponding column

        """
        column = self._data.columns
        return column[index]
        
    def detect(self, column: str):

        """
        This function detects the number of rows with NaN values in
        a given column.

        Parameters: 
            column (str): name of the column to be examined.

        Returns:
            nan_sum: amount of NaN values in a dataframe column.
        """
        
        nan_sum = self._data[column].isna().sum()

        print(nan_sum)
        return nan_sum


    def delete(self, columns:list):

        """
        This function deletes the rows containing NaN values on a group
        of given columns. 

        Parameters:
            columns (str): name of columns whoose nan rows are going to be removed.
        """

 
        new_df = self._data.dropna(subset=columns)
        new_df.reset_index(drop=True, inplace=True)
        self._data = new_df



    def replace(self, columns: list, value = 'mean'):

        """
        This function replaces NaN values with a constant, mean our median values
        for a given group of columns.

        Parameters:
            columns (list): group of columns whoose values are going to be replaced.
            value: 'mean' default (replaces with mean value) fo a given column.
                   'median' replaces with the median value.
                    custom value (float) choosen by user.
        """
        nan_cols = [c for c in columns if self.detect(c) > 0]

    
        if value == 'mean':
            sust_values = [self._data[c].mean() for c in nan_cols]
            
        elif value == 'median':
            sust_values = [self._data[c].median() for c in nan_cols]

        elif isinstance(value, int) or isinstance(value, float):
            sust_values = [value for _ in nan_cols]


        c_v_dict = dict(zip(nan_cols, sust_values))
        new_df = self._data.fillna(c_v_dict)
        self._data = new_df