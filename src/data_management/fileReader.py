"""Module for reading various file formats into pandas DataFrames."""

import pandas as pd
from pandas import DataFrame
import sqlite3
from pathlib import Path
import time


class ParseError(Exception):
    """Custom error for unsupported file formats."""
    pass

class FormatError(Exception):
    """Custom error for unsupported file formats."""
    pass


class FileReader:
    """Parses files and converts them into pandas DataFrames.
    
    Supports CSV, Excel, and SQLite database files.
    """

    def __init__(self):
        """Initialize FileReader with allowed file extensions."""
        self._allowed_extensions = {'.csv', '.xlsx', '.xls', '.db', '.sqlite'}

    def _check_format(self, extension: str) -> None:
        """Validate if file format is supported.
        
        Args:
            extension: File extension to validate.
            
        Raises:
            FormatError: If file extension is not supported.
        """
        if extension not in self._allowed_extensions:
            raise FormatError

    def parse_file(self, file_name: str) -> DataFrame:
        """Parse the given file into a pandas DataFrame.
        
        Args:
            file_name: Path to the file to be parsed.
            
        Returns:
            DataFrame containing the parsed data.
            
        Raises:
            Various exceptions based on file reading errors.
        """
        extension = Path(file_name).suffix

        try:
            self._check_format(extension)

            if extension == '.csv':
                df = pd.read_csv(file_name)
            elif extension in {'.xls', '.xlsx'}:
                df = pd.read_excel(file_name)
            elif extension in {'.db', '.sqlite'}:
                conn = sqlite3.connect(file_name)
                query = "SELECT name FROM sqlite_master WHERE type='table';"
                table_name = pd.read_sql(query, conn).iloc[0, 0]
                df = pd.read_sql(f'SELECT * FROM {table_name};', conn)
                conn.close()

            return df

        except FormatError:
            raise ParseError('ERROR: unsupported file format')
        except pd.errors.EmptyDataError:
            raise ParseError('ERROR: This file might be empty or corrupted')
        except pd.errors.ParserError:
            raise ParseError('ERROR: this file could not be parsed')
        except sqlite3.DatabaseError:
            raise ParseError('ERROR: an error occurred with your database')
        except sqlite3.OperationalError:
            raise ParseError('ERROR: could not access your database')
        except FileNotFoundError:
            raise ParseError('ERROR: file not found')
        except Exception as e:
            raise ParseError(f'ERROR: unknown error, could not read file')