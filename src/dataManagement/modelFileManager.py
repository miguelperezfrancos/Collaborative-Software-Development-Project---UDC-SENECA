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
    except Exception as e:
        print(f'ERROR: {e}')
        
        
def load_model(file_path: str):
    """
    This function loads a saved model from the specified file path.
    """
    try:
        model_data = joblib.load(file_path)
        
        # Acceder a cada elemento en el diccionario cargado
        formula = model_data.get('formula')
        input_column = model_data.get('x')
        output_column = model_data.get('y')
        r2 = model_data.get('r2')
        mse = model_data.get('mse')
        description = model_data.get('description')
        slope = model_data.get('slope')
        intercept = model_data.get('intercept')
        
        # Imprimir o devolver los datos como desees
        print("Formula:", formula)
        print("Input Column:", input_column)
        print("Output Column:", output_column)
        print("R^2:", r2)
        print("MSE:", mse)
        print("Description:", description)
        print("Slope:", slope)
        print("Intercept:", intercept)
        
        return model_data  # Puedes devolver el diccionario completo si lo necesitas

    except Exception as e:
        print("Error loading model:", e)