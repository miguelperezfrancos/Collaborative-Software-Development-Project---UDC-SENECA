"""
This module will create a linear regression using scikit learn
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

class Regression():

    def __init__():
        pass

    def make_model(self, input_col, output_col):

        # set the target and feature values
        x = df[['median_income']]
        y = df['median_house_value']

        # create and fit the model
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(X=x)

