import joblib
from typing import Dict

# Load the models from the .pkl file
models: Dict[str, object] = joblib.load('app/ml/models.pkl')

# Check if 'model' exists in the loaded models
if 'model' not in models:
    raise KeyError("'model' not found in models.pkl")

model = models['model']  # Assuming you have a model key

def update_with_ml_model(data: dict) -> dict:
    # Extract features from data
    features = [data['temperature'], data['humidity'], data['light_intensity'],
                data['noise'], data['co2'], data['pm25'], data['airflow']]

    # Reshape features to match the model input
    reshaped_features = [features]

    # Predict the energy and comfort
    predictions = model.predict(reshaped_features)
    data['energy'] = predictions[0][0]
    data['comfort'] = predictions[0][1]
    
    return data
