import pandas as pd #pandas will be used to read the files and transfer it to a data frame
from pandas import DataFrame
import sqlite3
from pathlib import Path #pathlib will allow us to figure out the extension of a file
import time

def nanoseconds():
    return time.perf_counter_ns()


class FormatError(Exception):
    "Custom error if the user chooses an unsuported file format"
    pass

class FileReader():

    """
    This class parses a file and converts it into a Pandas dataframe
    """

    def __init__(self):

        #we declare the permitted extensions 
        self._allowed_extensions = {'.csv', '.xlsx', '.xls', '.db', '.sqlite'}

    def _check_format(self, extension: str):

        """
        Make sure the choosen file is in one of the allowed formats, if not, we raise a Format Error

        parameters:
            extension (str): file extension
        """

        if extension not in self._allowed_extensions:
            raise FormatError 
        
    def parse_file(self, file_name: str) -> DataFrame:

        """
        This method parses the choosen file and cathces any erro that may occour 
        during the process.

        Parameters:
            file_name (str): name of file that is going to be parsed.
        
        Returns:
            df (pandas DataFrame): data frame containing all of the information parsed
        """

        t0 = nanoseconds()

        extension = Path(file_name).suffix #get the extension of the file

        try: #We use try/except to catch any errors that may occour while parsing files

            self._check_format(extension) #check that file format is valid

            if extension == '.csv':  #read csv files

                df = pd.read_csv(file_name)

            elif extension == '.xls' or extension == '.xlsx': #read excel files

                df = pd.read_excel(file_name)
                print('hey')

            elif extension == '.db' or extension == '.sqlite': 

                conn = sqlite3.connect(file_name) #stabllish connection with the database (SQLite)
                query = "SELECT name FROM sqlite_master WHERE type='table';" #We write this query to obtain the table name
                table_name = pd.read_sql(query, conn).iloc[0,0] #we execute that query and store it in the varibale table_name
                df = pd.read_sql(f'SELECT * FROM {table_name};', conn) #we sleect everything from that table and store it in a dataframe
                conn.close() #we close connection with our database

            tf = nanoseconds()

            print(f'reading time: {(tf-t0) / 1000000} miliseconds')

           
            return df

        #Trying to catch specific errors
        except FormatError:
            print('ERROR: unsupported file format')
        except pd.errors.EmptyDataError:
            print('ERROR: This file might be empty or corrupted')
        except pd.errors.ParserError:
            print('ERROR: this file could not be parsed')
        except sqlite3.DatabaseError:
            print("ERROR: an error occoured with your database")
        except sqlite3.OperationalError:
            print('ERROR: could not access to your database')
        except FileNotFoundError:
            print('ERROR: file not found')
        except: #catching any other errors
            print('ERROR: unknown error')            