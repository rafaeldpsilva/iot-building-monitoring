import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# Function to create the simple LSTM model
def train_consumption_model(dataframe, trained_model_path):
    df = dataframe[['Time', 'Consumption']].copy()

    # Convert 'Time' to datetime
    df['Time'] = pd.to_datetime(df['Time'])

    # Feature engineering
    df['year'] = df['Time'].dt.year
    df['month'] = df['Time'].dt.month
    df['day'] = df['Time'].dt.day
    df['hour'] = df['Time'].dt.hour
    df['minute'] = df['Time'].dt.minute
    df['second'] = df['Time'].dt.second

    # One-hot encoding
    encoded_df = pd.get_dummies(df, columns=['year', 'month', 'day', 'hour', 'minute', 'second'])

    # Split the dataset into features (X) and target (y)
    X = encoded_df.drop(columns=['Consumption', 'Time', 'second_0'] + encoded_df.filter(like='year_').columns.tolist())
    y = encoded_df['Consumption']

    # Scale the features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Define and train the Random Forest Regressor model
    rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
    rf_model.fit(X_train, y_train)

    # Make predictions
    y_pred_rf = rf_model.predict(X_test)

    # Calculate evaluation metrics for the Random Forest model
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mse_rf)
    r2_rf = r2_score(y_test, y_pred_rf)

    # Print evaluation metrics for the Random Forest model
    print(f'Random Forest Model MAE: {mae_rf}')
    print(f'Random Forest Model MSE: {mse_rf}')
    print(f'Random Forest Model RMSE: {rmse_rf}')
    print(f'Random Forest Model R-squared: {r2_rf}')

    # Define the file name using the timestamp
    filename = 'consumption.keras'

    # Create directory if it does not exist
    if not os.path.exists(trained_model_path):
        os.makedirs(trained_model_path)
        print(f"Created directory: {trained_model_path}")

    # Join the directory path and filename
    file_path = os.path.join(trained_model_path, filename)

    # Save the model
    joblib.dump(rf_model, file_path)
    print(f'Model saved to file: {file_path}')
    return file_path
