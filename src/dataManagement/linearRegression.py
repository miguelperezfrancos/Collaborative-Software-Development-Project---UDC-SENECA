"""
This module will create a linear regression using scikit learn
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt


class Model():

    """
    This class creates a regression model from
    a data set and an input of independent and target values.
    """

    def __init__(self):

        # attributes that are going to be saved
        self._formula = None
        self._y_name = None
        self._x_name = None
        self._slope = None
        self._intercept = None
        self._description = None
        self._r2 = None
        self._mse = None

        #attributes that are not going to be saved
        self._pred_line = None
        self._independent_value = None
        self._target_value = None

    # Property and setter for formula
    @property
    def formula(self):
        return self._formula
    
    @formula.setter
    def formula(self, value):
        self._formula = value
    
    # Property and setter for _model
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    # Property and setter for r2
    @property
    def r2(self):
        return self._r2

    @r2.setter
    def r2(self, value):
        self._r2 = value

    # property and setter for mse
    @property
    def mse(self):
        return self._mse

    @mse.setter
    def mse(self, value):
        self._mse = value

    # Property and setter for _pred_line
    @property
    def pred_line(self):
        return self._pred_line

    @pred_line.setter
    def pred_line(self, value):
        self._pred_line = value

    # Property and setter for _y_name
    @property
    def y_name(self):
        return self._y_name

    @y_name.setter
    def y_name(self, value):
        self._y_name = value

    # Property and setter for _x_name
    @property
    def x_name(self):
        return self._x_name

    @x_name.setter
    def x_name(self, value):
        self._x_name = value

    # Property and setter for _independent_value
    @property
    def independent_value(self):
        return self._independent_value

    @independent_value.setter
    def independent_value(self, value):
        self._independent_value = value

    # Property and setter for _target_value
    @property
    def target_value(self):
        return self._target_value

    @target_value.setter
    def target_value(self, value):
        self._target_value = value

    # Property and setter for the slope
    @property
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, value):
        self._slope = value

    # Property and setter for the intercept
    @property
    def intercept(self):
        return self._intercept

    @intercept.setter
    def intercept(self, value):
        self._intercept = value

    #Property and setter for description
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
        

    def create_from_data(self, data: pd.DataFrame, input_col: str, output_col: str):
        """
        This function creates a linear regression model.

        Parameters:
            data (pandas DataFrame): data used for the regression.
            input-col (str): feature variable.
            output_col (str): target variable.
        """

        # set the variable names for our model
        self._x_name = input_col
        self._y_name = output_col

        # set the target and feature values
        self._independent_value = data[[input_col]]
        self._target_value = data[output_col]

        # create and fit the model
        r_model = LinearRegression()
        r_model.fit(self._independent_value, self._target_value)
        y_pred = r_model.predict(X=self._independent_value)

        # asign the model, slope and intercept to the class variables
        self._pred_line = y_pred
        self._slope = r_model.coef_[0]
        self._intercept = r_model.intercept_

        #assign r2 and mse
        self._mse = mean_squared_error(self._target_value, self._pred_line)
        self._r2 = r2_score(self._target_value, self._pred_line)
        self._formula = f'{self._y_name} = {self._slope:.2f} * {self._x_name} + {self._intercept:.2f}'


    def get_plot(self):

        """
        This function creates a graph for the linear regression it has made.
        """

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(self._independent_value, self._target_value, color='blue', label='Actual Data')
        ax.plot(self._independent_value, self._pred_line, color='red', label='Regression Line')
        
        # Labels and title
        ax.set_xlabel(self._x_name)
        ax.set_ylabel(self._y_name)
        ax.set_title("Linear Regression Plot")
        ax.legend()
        ax.grid(True)
        
        return fig  # Return the figure object