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

    def get_plot_text(self):
        """
        Devuelve el texto con la fórmula de predicción, R² y MSE.
        
        Returns:
            plot_text (str): Texto que contiene la fórmula de predicción, R² y MSE formateado.
        """
        formula_text = self.get_regression_line()
        r2 = self.get_r_squared()
        mse = self.get_MSE()
        
        # Formatear el texto para visualizar fuera de la gráfica
        plot_text = (
            f"Prediction Formula: {formula_text}\n"
            f"R²: {r2:.2f}\n"
            f"MSE: {mse:.2f}"
        )
        return plot_text

    def get_plot(self):
        """
        This function creates a graph for the linear regression it has made,
        ensuring consistent axis scaling and optimal data representation.
        """

        # Crear la figura cuadrada con un tamaño que permita la visualización correcta del texto
        fig, ax = plt.subplots(figsize=(12, 8))

        # Graficar datos y línea de regresión
        ax.scatter(self._independent_value, self._target_value, color='blue', label='Actual Data')
        ax.plot(self._independent_value, self._pred_line, color='red', label='Regression Line')

        # Ajuste automático de los límites de los datos y escalado de ejes
        ax.relim()
        ax.autoscale_view()

        # Asegurar que el aspecto de los ejes mantenga la proporción de los datos
        x_range = self._independent_value.max().iloc[0] - self._independent_value.min().iloc[0]
        y_range = max(self._target_value.max(), self._pred_line.max()) - min(self._target_value.min(), self._pred_line.min())
        ax.set_aspect(aspect=x_range / y_range, adjustable='datalim')

        # Configuración de textos
        formula_text = self.get_regression_line()
        r2 = self.get_r_squared()
        mse = self.get_MSE()
        # Etiquetas, leyenda y cuadrícula
        ax.set_xlabel(self._x_name)
        ax.set_ylabel(self._y_name)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)

        return fig  # Retornar la figura


    


