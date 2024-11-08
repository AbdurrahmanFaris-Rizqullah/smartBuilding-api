import joblib
import pandas as pd

# Memuat model machine learning
models = joblib.load('app/ml/models.pkl')
energy_model = models['energy_model']
comfort_model = models['comfort_model']
scaler = joblib.load('app/ml/scaler.pkl')

def update_with_ml_model(data):
    X = pd.DataFrame([data])
    X_scaled = scaler.transform(X)

    # Prediksi menggunakan model machine learning
    energy_pred = energy_model.predict(X_scaled)
    comfort_pred = comfort_model.predict(X_scaled)

    # Perbarui data dengan prediksi baru
    data['energy'] = energy_pred[0]
    data['comfort'] = comfort_pred[0]

    return data
