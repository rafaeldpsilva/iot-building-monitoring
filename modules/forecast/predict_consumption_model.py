import os
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta


def average_by_pairs_of_4(data):
    # Ensure the length of data is a multiple of 4 for even pairing
    if len(data) % 4 != 0:
        raise ValueError("The length of data must be a multiple of 4.")

    # Reshape the data into pairs of 4 and calculate the average
    reshaped_data = data.reshape(-1, 4)
    averages = reshaped_data.mean(axis=1)

    return averages


def predict_hours_con(dataframe, con_model_path, start_time, num_hours_to_predict):
    # Load the dataset
    df = dataframe.copy()

    # Select only the "Time" and "Generation" columns
    df = df[['Time', 'Consumption']]

    # Convert 'Time' column to datetime type
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
    X = encoded_df.drop(columns=['Consumption', 'Time', 'second_0'] + encoded_df.filter(like='year_').columns.tolist())
    y = encoded_df['Consumption']
    X_columns = X.columns
    # Scale the features using MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Load the model using joblib
    if not os.path.exists(con_model_path):
        raise FileNotFoundError(f"The model file {con_model_path} does not exist.")
    try:
        model = joblib.load(con_model_path)
    except Exception as e:
        raise ValueError(f"Error loading the model file: {e}")

    num_intervals = num_hours_to_predict * 4
    # Create a DataFrame to hold the future times
    future_times = [start_time + timedelta(minutes=15 * i) for i in range(num_intervals)]
    hourly_times = [start_time + timedelta(hours=i) for i in range(num_hours_to_predict)]
    future_df = pd.DataFrame({'Time': future_times})

    # Extract relevant components
    future_df['year'] = future_df['Time'].dt.year
    future_df['month'] = future_df['Time'].dt.month
    future_df['day'] = future_df['Time'].dt.day
    future_df['hour'] = future_df['Time'].dt.hour
    future_df['minute'] = future_df['Time'].dt.minute
    future_df['second'] = future_df['Time'].dt.second

    # Perform one-hot encoding on each component
    future_encoded_df = pd.get_dummies(future_df, columns=['year', 'month', 'day', 'hour', 'minute', 'second'])

    # Ensure the future encoded DataFrame has the same columns as the training data
    for col in X_columns:
        if col not in future_encoded_df.columns:
            future_encoded_df[col] = 0

    # Scale the features using the previously fitted scaler
    future_scaled = scaler.transform(future_encoded_df[X_columns])

    # Make predictions
    future_predictions = model.predict(future_scaled)
    hourly_preds = average_by_pairs_of_4(future_predictions)

    return future_times, future_predictions, hourly_times, hourly_preds


def predict_con_24_hours_from_now(dataframe, rfr_model_path):
    today = datetime.now()
    start_time = datetime(today.year, today.month, today.day) + timedelta(days=1)
    num_hours_to_predict = 24
    return predict_hours_con(dataframe=dataframe, con_model_path=rfr_model_path, start_time=start_time,
                             num_hours_to_predict=num_hours_to_predict)


if __name__ == "__main__":
    hours_24 = True
    # Load the dataframe from a CSV file
    dataset = pd.read_csv('../datasets/Community.csv')
    model_path = './trained_models/con_RFR_model_1720537334433.pkl'
    if hours_24:
        future_times, future_predictions, hourly_times, hourly_preds = predict_con_24_hours_from_now(dataframe=dataset,
                                                                                                     rfr_model_path=model_path)
        print("Future times:", future_times)
        print("Future predictions:", future_predictions)
        print("Hourly times:", hourly_times)
        print("Hourly predictions:", hourly_preds)
    else:
        today = datetime.now()
        print(today)
        start_time = datetime(today.year, today.month, today.day, today.hour) + timedelta(hours=1)
        num_hours_to_predict = 1
        ft, future_predictions, ht, hourly_preds = predict_hours_con(
            dataframe=dataset,
            con_model_path=model_path,
            start_time=start_time,
            num_hours_to_predict=num_hours_to_predict
        )
        future_times = ft
        hourly_times = ht
        print("Future times:", future_times)
        print("Future predictions:", future_predictions)
        print("Hourly times:", hourly_times)
        print("Hourly predictions:", hourly_preds)
