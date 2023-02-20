from modules.forecast.consumption_forecast import consumption_forecast

class ForecastAdapter:
    def __init__(self):
        return
    
    def forecast_day_consumption(self,consumption):
        return consumption_forecast(consumption)