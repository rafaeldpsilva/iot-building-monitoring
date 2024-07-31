import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import datetime
import os


# Function to create the simple LSTM model
def train_generation_model(dataframe, trained_model_path):
    df = dataframe[['Time', 'Generation']].copy()
    numerical_columns = ['Time', 'Generation']
    # Convert 'datetime' column to datetime type
    df['Time'] = pd.to_datetime(df['Time'])

    # Extract relevant components
    df['year'] = df['Time'].dt.year
    df['month'] = df['Time'].dt.month
    df['day'] = df['Time'].dt.day
    df['hour'] = df['Time'].dt.hour
    df['minute'] = df['Time'].dt.minute
    df['second'] = df['Time'].dt.second

    # Perform one-hot encoding on each component
    encoded_df = pd.get_dummies(df, columns=['year', 'month', 'day', 'hour', 'minute', 'second'])
    # Split the dataset into features (X) and target (y)
    X = encoded_df.drop(columns=['Generation', 'Time', 'second_0'] + encoded_df.filter(like='year_').columns.tolist())
    y = encoded_df['Generation']

    # Scale the features using MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Reshape the data to 3D array for LSTM (samples, timesteps, features)
    X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.2, random_state=42)

    # Train and evaluate the simple model
    model = Sequential()
    model.add(LSTM(50, activation='tanh', input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1, activation='relu'))
    model.compile(optimizer='adam', loss='mse')
    history_simple = model.fit(X_train, y_train, epochs=1, batch_size=64, validation_data=(X_test, y_test),
                               verbose=1)

    y_pred_simple = model.predict(X_test)

    # Calculate evaluation metrics for the simple model
    mae_simple = mean_absolute_error(y_test, y_pred_simple)
    mse_simple = mean_squared_error(y_test, y_pred_simple)
    rmse_simple = np.sqrt(mse_simple)
    r2_simple = r2_score(y_test, y_pred_simple)

    # Print evaluation metrics for the simple model
    print(f'Simple Model MAE: {mae_simple}')
    print(f'Simple Model MSE: {mse_simple}')
    print(f'Simple Model RMSE: {rmse_simple}')
    print(f'Simple Model R-squared: {r2_simple}')

    # Define the file name using the timestamp
    filename = 'generation.keras'

    # Create directory if it does not exist
    if not os.path.exists(trained_model_path):
        os.makedirs(trained_model_path)
        print(f"Created directory: {trained_model_path}")

    # Join the directory path and filename
    file_path = os.path.join(trained_model_path, filename)

    # Save the model
    model.save(file_path)
    print(f'Model saved to file: {file_path}')
    return file_path
