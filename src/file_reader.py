import pandas as pd #pandas will be used to read the files and transfer it to a data frame
from pandas import DataFrame
import sqlite3
from pathlib import Path #pathlib will allow us to figure out the extension of a file

class FormatError(Exception):
    "Custom error if the user chooses an unsuported file format"
    pass

class FileReader():

    def __init__(self):

        self._allowed_extensions = {'.csv', '.xlsx', '.xls', '.db', '.sqlite'}

    def _check_format(self, extension):

        if extension not in self._allowed_extensions:
            raise FormatError 
        
    def parse_file(self, file_name: str) -> DataFrame:

        extension = Path(file_name).suffix #get the extension of the file

        try: #We use try/except to catch any errors that may occour while parsing files

            self._check_format(extension) #check that file format is valid

            if extension == '.csv':  #read csv files

                df = pd.read_csv(file_name)

            elif extension == '.xls' or extension == '.xlsx': #read excel files

                df = pd.read_excel(file_name)

            elif extension == '.db' or extension == '.sqlite': 

                conn = sqlite3.connect(file_name) #stabllish connection with the database (SQLite)
                query = "SELECT name FROM sqlite_master WHERE type='table';" #We write this query to obtain the table name
                table_name = pd.read_sql(query, conn).iloc[0,0] #we execute that query and store it in the varibale table_name
                df = pd.read_sql(f'SELECT * FROM {table_name};', conn) #we sleect everything from that table and store it in a dataframe
                conn.close() #we close connection with our database

            print(f'\n{df.head(10)}')
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

if __name__ == "__main__":

    file_name = file_name = input('Enter a file name (supported formats: csv, Excel and SQLite):  ')
    reader = FileReader()
    data_frame = reader.parse_file(file_name=file_name)