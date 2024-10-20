import numpy as np
import pandas as pd
from dataManager import DataManager as dm

if __name__ == '__main__':

    # Set a random seed for reproducibility
    np.random.seed(42)

    # Create a 10x5 DataFrame with random numbers
    df = pd.DataFrame(np.random.rand(10, 5), columns=list('ABCDE'))

    # Introduce NaN values randomly in the DataFrame
    nan_indices = [(np.random.randint(10), np.random.randint(5)) for _ in range(10)]
    for row, col in nan_indices:
        df.iat[row, col] = np.nan

    print(df)

    mydm = dm()
    mydm.data = df

    #mydm.replace(columns=['E', 'D'], value='median')
    mydm.delete(columns=['C', 'D'])

    print('')
    print(mydm.data)

