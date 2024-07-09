import tensorflow as tf
import joblib
from datetime import timedelta
import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
sys.path.append('.')
from database.BuildingRepository import BuildingRepository

def create_model():
    look_back = 15
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)


def train_model(df):
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)

    # Select the columns to be used for prediction
    data = df[['Consumption']]

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    look_back = 15

    # Prepare data for consumption prediction
    X_con, y_con = create_dataset(scaled_data[:, 0].reshape(-1, 1), look_back)

    X_con = np.reshape(X_con, (X_con.shape[0], look_back, 1))
    model = create_model()
    model.fit(X_con, y_con, batch_size=1, epochs=10)
    model.save("modules/forecast/consumption.keras")

    # Make predictions for Consumption
    predictions_con = model.predict(X_con)
    predictions_con = scaler.inverse_transform(
        np.concatenate((np.zeros_like(predictions_con), predictions_con), axis=1))[:, 1]

def prepare_data(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps - 2):
        X.append(data[i:i + time_steps, :-1])  # Exclude the last column (Consumption)
        y.append(data[i + time_steps, -1])  # The last column (Consumption) is the target
    return np.array(X), np.array(y)

def predict_saved_model(last_24_hours_data):
    model = tf.keras.models.load_model('saved_model/consumption_forecast')

    # Load the scaler
    scaler = joblib.load('saved_model/scaler.pkl')
    pred_scaler = joblib.load('saved_model/pred_scaler.pkl')

    df_scaled = scaler.fit_transform(last_24_hours_data)
    
    timesteps = 1
    X_pred, y = prepare_data(df_scaled, timesteps)
    X_pred = np.reshape(X_pred, (X_pred.shape[0], timesteps, X_pred.shape[2]))
    
    y_pred = model.predict(X_pred)
    y_pred = pred_scaler.inverse_transform(y_pred)

    last = scaler.inverse_transform(df_scaled[:-3])

    df = pd.DataFrame(last, columns=['Month', 'Day', 'Hour', 'Minute', 'Consumption-1', 'Consumption-2', 'Consumption'])
    df['Prediction'] = y_pred
    df['datetime'] = pd.to_datetime(df[['Month', 'Day', 'Hour', 'Minute']].assign(Year=2023))

    # Drop the separate columns if needed
    df.drop(['Month', 'Day', 'Hour', 'Minute'], axis=1, inplace=True)

    df.set_index("datetime", inplace=True)
    df = df.resample('1H').mean()
    df["datetime"] = df.index

    return df

def forecast_consumption():
    building_repo = BuildingRepository()

    df_test = pd.DataFrame(building_repo.get_totalpower_col())
    df_test = df_test.drop("_id", axis=1)

    df_test['datetime'] = pd.to_datetime(df_test['datetime'])

    current_time = df_test['datetime'].max()
    twenty_four_hours_ago = current_time - timedelta(hours=24)

    last_24_hours_data = df_test[df_test['datetime'] >= twenty_four_hours_ago]

    last_24_hours_data['totalpower'] = pd.to_numeric(last_24_hours_data['totalpower'], errors='coerce')
    last_24_hours_data['Month'] = last_24_hours_data['datetime'].dt.month
    last_24_hours_data['Day'] = last_24_hours_data['datetime'].dt.day
    last_24_hours_data['Hour'] = last_24_hours_data['datetime'].dt.hour
    last_24_hours_data['Minute'] = last_24_hours_data['datetime'].dt.minute

    last_24_hours_data.rename(columns={'totalpower': 'Consumption'}, inplace=True)
    last_24_hours_data.drop(['datetime', 'totalgeneration'], axis=1, inplace=True)

    last_24_hours_data = last_24_hours_data.dropna()
    last_24_hours_data['Consumption-1'] = last_24_hours_data['Consumption'].shift(1)
    last_24_hours_data.loc[last_24_hours_data['Day'] != last_24_hours_data['Day'].shift(1), 'Consumption-1'] = 0
    last_24_hours_data['Consumption-2'] = last_24_hours_data['Consumption'].shift(2)
    last_24_hours_data.loc[last_24_hours_data['Day'] != last_24_hours_data['Day'].shift(2), 'Consumption-2'] = 0
    last_24_hours_data = last_24_hours_data[
        ['Month', 'Day', 'Hour', 'Minute', 'Consumption-1', 'Consumption-2', 'Consumption']]

    return predict_saved_model(last_24_hours_data)


