import joblib

"""
This module will take care of saving and parsing 
joblib files.
"""

def save_model(file_path: str, formula:str, input: str, output:str,
               r2:int, mse: int, description: str, slope: int, intercept: int):
    
    """
    This function saves a model.
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
    except:
        Exception


def load_model():
    pass