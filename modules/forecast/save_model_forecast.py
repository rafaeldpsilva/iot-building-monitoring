import tensorflow as tf
import joblib
from datetime import timedelta
import pandas as pd
import numpy as np
from database.BuildingRepository import BuildingRepository

def prepare_data(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps - 2):
        X.append(data[i:i + time_steps, :-1])  # Exclude the last column (Consumption)
        y.append(data[i + time_steps, -1])  # The last column (Consumption) is the target
    return np.array(X), np.array(y)

def predict_saved_model(last_24_hours_data):
    model = tf.keras.models.load_model('saved_model/consumption_forecast')

    # Load the scaler
    scaler_test = joblib.load('training_1/scaler.pkl')
    pred_scaler = joblib.load('training_1/pred_scaler.pkl')

    df_scaled = scaler_test.fit_transform(last_24_hours_data)
    
    timesteps = 1
    X_pred, y = prepare_data(df_scaled, timesteps)
    X_pred = np.reshape(X_pred, (X_pred.shape[0], timesteps, X_pred.shape[2]))
    
    y_pred = model.predict(X_pred)
    y_pred = pred_scaler.inverse_transform(y_pred)
    return y_pred