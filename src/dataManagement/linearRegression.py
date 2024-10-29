"""
This module will create a linear regression using scikit learn
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt


class Regression():

    def __init__(self):

        self._model = None
        self._pred_line = None
        self._y_name = None
        self._x_name = None
        self._independent_value = None
        self._target_value = None

    def make_model(self, data: pd.DataFrame, input_col: str, output_col: str):
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

        # asign the model to the class variables
        self._model = r_model
        self._pred_line = y_pred

    def get_regression_line(self):
        """
        This function returns the regression line definition as a string.

        Returns:
            model_line (str): string containing the regression model line
        """
        slope = self._model.coef_[0]
        intercept = self._model.intercept_

        model_line = f'{self._y_name} = {slope:.2f} * {self._x_name} + {intercept:.2f}'

        return model_line

    def get_r_squared(self):
        """
        This funciton returns the R² measure of our regression model.

        Returns:
            r_squared
        """
        r2 = r2_score(self._target_value, self._pred_line)
        return r2

    def get_MSE(self):
        """
        This funciton returns the mean squared error (MSE) measure of our regression model.

        Returns:
            MSE
        """
        MSE = mean_squared_error(self._target_value, self._pred_line)
        return MSE

    def plot_regression(self, X: str, y: str, model, MSE, r2):
        """
        Plot the regression results.

        Args:
        X (str): Feature variable.
        y (str): Target variable.
        model (LinearRegression): Fitted linear regression model.
        MSE (float): Mean Squared Error.
        r2 (float): R² score.
        """

        plt.figure(figsize=(10, 6))
        plt.scatter(self._independent_value, self._target_value,
                    color='blue', alpha=0.5, label='Data')
        plt.plot(self._independent_value, model.predict(
            self._independent_value), color='red', label='Regression Line')
        plt.xlabel(f'{X}')
        plt.ylabel(f'{y}')
        plt.title('Linear Regression Model')
        plt.legend()

        # Display formula and metrics
        formula = f"{y} = {model.coef_[0][0]:.2f}{X} + {model.intercept_[0]:.2f}"
        metrics = f"Mean Squared Error: {MSE:.2f}\nR² Score: {r2:.2f}"
        plt.text(0.05, 0.95, formula, transform=plt.gca().transAxes,
                 verticalalignment='top', fontsize=10)
        plt.text(0.05, 0.85, metrics, transform=plt.gca().transAxes,
                 verticalalignment='top', fontsize=10)

        plt.tight_layout()
        plt.show()