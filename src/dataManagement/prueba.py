import pandas as pd
from dataManager import DataManager as dm

if __name__ == '__main__':

    mydm = dm()
    mydm.data = pd.read_csv('/Users/rafa/Documents/IT/gasStation/gas_prices.csv')
    print(mydm.data.head())
    mydm.detect(column='price_gasoleo_b')

