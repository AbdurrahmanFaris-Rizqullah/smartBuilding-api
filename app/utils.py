import joblib
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

# Load the models from the .pkl file
models: Dict[str, object] = joblib.load('app/ml/models.pkl')

# Check if both models exist in the loaded models
if 'energy_model' not in models or 'comfort_model' not in models:
    raise KeyError("'energy_model' or 'comfort_model' not found in models.pkl")

energy_model = models['energy_model']
comfort_model = models['comfort_model']

class InputData(BaseModel):
    people: int
    temperature: float
    humidity: float
    lightIntensity: int
    noise: int
    co2: int
    pm25: float
    airflow: float

def update_with_ml_model(data: dict) -> dict:
    # Extract features from data
    features = [data['people'], data['temperature'], data['humidity'], data['lightIntensity'],
                data['noise'], data['co2'], data['pm25'], data['airflow']]

    # Reshape features to match the model input
    reshaped_features = [features]

    # Predict the energy and comfort
    energy_prediction = energy_model.predict(reshaped_features)
    comfort_prediction = comfort_model.predict(reshaped_features)

    data['energy'] = energy_prediction[0]
    data['comfort'] = comfort_prediction[0]

    return data