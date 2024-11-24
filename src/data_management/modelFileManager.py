"""Module for handling model file operations using joblib.

This module provides functionality for saving and loading model data
using joblib serialization.
"""

import joblib
from data_management import Model


def save_model(file_path: str, formula: str, input: str, output: str,
    r2: float, mse: float, description: str, slope: float, intercept: float
) -> None:
    """Save a model's data to a file using joblib.

    Args:
        file_path: Path where the model will be saved
        formula: Mathematical formula of the model
        input: Input variable name
        output: Output variable name
        r_squared: R-squared value of the model
        mse: Mean squared error of the model
        description: Model description
        slope: Slope coefficient
        intercept: Intercept value

    Returns:
        None
    """
    model_data = {
        'formula': formula,
        'x': input,
        'y': output,
        'r2': r2,
        'mse': mse,
        'description': description,
        'slope': slope,
        'intercept': intercept
    }

    try:
        joblib.dump(model_data, file_path)
    except Exception as e:
        print(f'Error saving model: {e}')


def load_model(file_path: str) -> Model | None:
    """Load a saved model from a file.

    Args:
        file_path: Path to the saved model file

    Returns:
        Model: Loaded model object if successful, None otherwise
    """
    try:
        model_data = joblib.load(file_path)
        model = Model()

        model.formula = model_data.get('formula')
        model.x_name = model_data.get('x')
        model.y_name = model_data.get('y')
        model.r2 = model_data.get('r2')
        model.mse = model_data.get('mse')
        model.description = model_data.get('description')
        model.slope = model_data.get('slope')
        model.intercept = model_data.get('intercept')

        return model

    except Exception as e:
        raise ValueError('Unable to read file')
        print(f"Error loading model: {e}")
        return None