import pandas as pd


class ForecastAdapter:
    def __init__(self):
        self.models_dir = './modules/forecast/trained_models'
        self.consumption_model_path = self.models_dir + '/consumption.keras'
        self.generation_model_path = self.models_dir + '/generation.keras'

    def train_consumption_model(self, consumption):
        from modules.forecast.train_consumption_model import train_consumption_model

        consumption = consumption.rename(columns={'totalpower': 'Consumption', 'datetime': 'Periods'})
        consumption = pd.DataFrame(consumption, columns=['Time', 'Consumption'])

        self.consumption_model_path = train_consumption_model(consumption, self.models_dir)

    def train_generation_model(self, generation):
        from modules.forecast.train_consumption_model import train_consumption_model

        generation = generation.rename(columns={'totalpower': 'Generation', 'datetime': 'Periods'})
        generation = pd.DataFrame(generation, columns=['Time', 'Generation'])

        self.generation_model_path = train_consumption_model(generation, self.models_dir)

    def forecast_day_consumption(self, consumption):
        from modules.forecast.predict_consumption_model import predict_con_24_hours_from_now

        consumption = consumption.rename(columns={'totalpower': 'Consumption', 'datetime': 'Periods'})
        consumption = pd.DataFrame(consumption, columns=['Time', 'Consumption'])
        future_times, future_predictions, hourly_times, hourly_preds = predict_con_24_hours_from_now(consumption, self.consumption_model_path)

    def forecast_day_generation(self, generation):
        from modules.forecast.predict_generation_model import predict_gen_24_hours_from_now

        generation = generation.rename(columns={'totalpower': 'Generation', 'datetime': 'Periods'})
        generation = pd.DataFrame(generation, columns=['Time', 'Generation'])
        future_times, future_predictions, hourly_times, hourly_preds = predict_gen_24_hours_from_now(generation, self.generation_model_path)
