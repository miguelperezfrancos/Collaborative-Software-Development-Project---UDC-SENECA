import joblib
from dataManagement import Model

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
    except Exception as e:
        print(f'ERROR: {e}')
        
        
def load_model(file_path: str):
    """
    This function loads a saved model from the specified file path.
    """
    try:
        model_data = joblib.load(file_path)
        model = Model()
        
        # Acceder a cada elemento en el diccionario cargado
        model.formula = model_data.get('formula')
        model.x_name = model_data.get('x')
        model.y_name = model_data.get('y')
        model.r2 = model_data.get('r2')
        model.mse = model_data.get('mse')
        model.description = model_data.get('description')
        model.slope = model_data.get('slope')
        model.intercept = model_data.get('intercept')
        
        return model  # Puedes devolver el diccionario completo si lo necesitas

    except Exception as e:
        print("Error loading model:", e)