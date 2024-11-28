"""Module for creating and visualizing linear regression models using scikit-learn."""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

class UnexpectedError(Exception):
    """Exception raised for unexpected errors."""
    pass


class Model:
    """Creates and manages linear regression models from datasets."""

    def __init__(self):
        """Initialize model attributes."""
        # Persistent attributes
        self._formula = None
        self._y_name = None
        self._x_name = None
        self._slope = None
        self._intercept = None
        self._description = None
        self._r2 = None
        self._mse = None

        # Temporary attributes
        self._pred_line = None
        self._independent_value = None
        self._target_value = None

    @property
    def formula(self):
        """Get the regression formula."""
        return self._formula

    @formula.setter
    def formula(self, value):
        self._formula = value

    @property
    def r2(self):
        """Get R-squared value."""
        return self._r2

    @r2.setter
    def r2(self, value):
        self._r2 = value

    @property
    def mse(self):
        """Get mean squared error."""
        return self._mse

    @mse.setter
    def mse(self, value):
        self._mse = value

    @property
    def pred_line(self):
        """Get prediction line values."""
        return self._pred_line

    @pred_line.setter
    def pred_line(self, value):
        self._pred_line = value

    @property
    def y_name(self):
        """Get dependent variable name."""
        return self._y_name

    @y_name.setter
    def y_name(self, value):
        self._y_name = value

    @property
    def x_name(self):
        """Get independent variable name."""
        return self._x_name

    @x_name.setter
    def x_name(self, value):
        self._x_name = value

    @property
    def independent_value(self):
        """Get independent variable values."""
        return self._independent_value

    @independent_value.setter
    def independent_value(self, value):
        self._independent_value = value

    @property
    def target_value(self):
        """Get target variable values."""
        return self._target_value

    @target_value.setter
    def target_value(self, value):
        self._target_value = value

    @property
    def slope(self):
        """Get regression slope."""
        return self._slope

    @slope.setter
    def slope(self, value):
        self._slope = value

    @property
    def intercept(self):
        """Get regression intercept."""
        return self._intercept

    @intercept.setter
    def intercept(self, value):
        self._intercept = value

    @property
    def description(self):
        """Get model description."""
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def create_from_data(self, data: pd.DataFrame, input_col: str, 
                         output_col: str) -> None:
        """Create a linear regression model from input data.
        
        Args:
            data: DataFrame containing the data.
            input_col: Name of the independent variable column.
            output_col: Name of the dependent variable column.
        """

        try:
            #Fit the model first so it doesn't change the pre-existing model
            r_model = LinearRegression()
            r_model.fit(data[[input_col]], data[output_col])

            #Start to update
            self._x_name = input_col
            self._y_name = output_col
            self._description = None

            self._independent_value = data[[input_col]]
            self._target_value = data[output_col]
            y_pred = r_model.predict(X=self._independent_value)
            self._pred_line = y_pred

            self._slope = r_model.coef_[0]
            self._intercept = r_model.intercept_

            self._mse = mean_squared_error(self._target_value, self._pred_line)
            self._r2 = r2_score(self._target_value, self._pred_line)
            self._formula = (
                f'{self._y_name} = {self._slope:.2f} * {self._x_name} + '
                f'{self._intercept:.2f}'
            )

        except Exception as e:

            raise UnexpectedError(e)

    def get_plot(self) -> plt.Figure:
        """Create and return a visualization of the regression model.
        
        Returns:
            Matplotlib figure containing the regression plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=(1, 1, 1, 0))

        ax.scatter(
            self._independent_value,
            self._target_value,
            s=10,
            color='#c2ffff',
            alpha=0.7
        )
        ax.plot(self._independent_value, self._pred_line, color='#E74C3C')

        ax.set_xlabel(self._x_name, color='#a0a0a0')
        ax.set_ylabel(self._y_name, color='#a0a0a0')

        ax.tick_params(axis='x', colors='#a0a0a0')
        ax.tick_params(axis='y', colors='#a0a0a0')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(True)

        ax.grid(False)
        plt.tight_layout()

        ax.patch.set_alpha(0.0)

        return fig