"""Module for managing data operations and transformations.

This module provides a DataManager class for handling data operations,
including NaN detection and handling.
"""

from typing import List, Union, Optional
import pandas as pd


class DataManager:
    """Class for managing data operations and transformations.

    This class implements methods and variables needed by the application
    for operating with user-loaded data and maintains the data model
    shown on the interface.
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """Initialize DataManager with optional data.

        Args:
            data: Initial pandas DataFrame (optional)
        """
        self._data = data

    @property
    def data(self) -> pd.DataFrame:
        """Get the current DataFrame.

        Returns:
            The stored DataFrame
        """
        return self._data

    @data.setter
    def data(self, new_data: pd.DataFrame) -> None:
        """Set a new DataFrame.

        Args:
            new_data: New DataFrame to store

        Raises:
            ValueError: If new_data is not a pandas DataFrame
        """
        if isinstance(new_data, pd.DataFrame):
            self._data = new_data
        else:
            raise ValueError('Data must be a pandas DataFrame')

    def get_columns(self, index: int) -> str:
        """Get column name by index.

        Args:
            index: Index of the column to retrieve

        Returns:
            Name of the corresponding column
        """
        columns = self._data.columns
        return columns[index]

    def detect(self, column: str) -> int:
        """Count NaN values in a column.

        Args:
            column: Name of the column to examine

        Returns:
            Number of NaN values in the column
        """
        nan_count = self._data[column].isna().sum()
        return nan_count

    def delete(self, columns: List[str]) -> None:
        """Delete rows containing NaN values in specified columns.

        Args:
            columns: List of column names whose NaN rows should be removed
        """
        new_df = self._data.dropna(subset=columns)
        new_df.reset_index(drop=True, inplace=True)
        self._data = new_df

    def replace(self, columns: List[str], 
                value: Union[str, int, float] = 'mean') -> None:
        """Replace NaN values in specified columns.

        Args:
            columns: List of columns whose values should be replaced
            value: Replacement strategy or value:
                  'mean' (default) - replace with column mean
                  'median' - replace with column median
                  number - replace with specific value
        """
        nan_cols = [col for col in columns if self.detect(col) > 0]


        if value == 'mean':
            replacement_values = [self._data[col].mean() for col in nan_cols]
        elif value == 'median':
            replacement_values = [self._data[col].median() for col in nan_cols]
        elif isinstance(value, (int, float)):
            replacement_values = [value for _ in nan_cols]
        else:
            return

        col_value_dict = dict(zip(nan_cols, replacement_values))

        try:
            new_df = self._data.fillna(col_value_dict)
            self._data = new_df
        except:
            raise Exception  # Maintain current state if replacement fails