import pandas as pd
class ForecastAdapter:
    def __init__(self):
        return
    
    def forecast_saved_model(self, last_24_hours_data):
        from modules.forecast.save_model_forecast import predict_saved_model
        return predict_saved_model(last_24_hours_data)
        
    def forecast_day_consumption(self, consumption):
        from modules.forecast.Forecast_Script_Consumption import ForecastDay_Cons
    
        consumption = consumption.rename(columns={'totalpower': 'Consumption', 'datetime': 'Periods'})
        consumption = pd.DataFrame(consumption, columns=['Periods', 'Consumption'])
        return ForecastDay_Cons(consumption)

    def forecast_consumption(self,consumption):
        from modules.forecast.consumption_forecast import consumption_forecast
        forecast = consumption_forecast(consumption)
        #building_repo.insert_forecastday(Pred.iat, datetime.datetime.now() + datetime.timedelta(minutes=45))
        return forecast