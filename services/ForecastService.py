from database.BuildingRepository import BuildingRepository
from modules.ForecastAdapter import ForecastAdapter
import pandas as pd 
from datetime import datetime, timedelta

class ForecastService:
    def __init__(self):
        self.building_repo = BuildingRepository()

    def forecast_consumption(self):
        building_repo = BuildingRepository()
        now = datetime.now()
        start = now - timedelta(days=7, hours=now.hour, minutes=now.minute)
        building_totalpower = building_repo.get_historic_hour_interval(start, start + timedelta(days=1))
        consumption = []
        for line in building_totalpower:
            consumption.append([line['datetime'],line['consumption']])

        total = pd.DataFrame(consumption, columns=['datetime', 'consumption'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1h').mean()
        return total['consumption'].values.tolist()

    def forecast_generation(self):
        building_repo = BuildingRepository()
        now = datetime.now()
        start = now - timedelta(days=1, hours=now.hour, minutes=now.minute)
        building_totalpower = building_repo.get_historic_hour_interval(start, start + timedelta(days=1))
        generation = []
        for line in building_totalpower:
            generation.append([line['datetime'],line['generation']])

        total = pd.DataFrame(generation, columns=['datetime', 'generation'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1h').mean()
        return total['generation'].values.tolist()

    def forecast_flexibility(self):
        building_repo = BuildingRepository()
        now = datetime.now()
        start = now - timedelta(days=1, hours=now.hour, minutes=now.minute)
        building_totalpower = building_repo.get_historic_hour_interval(start, start + timedelta(days=1))
        flexibility = []
        for line in building_totalpower:
            flexibility.append([line['datetime'],line['flexibility']])

        total = pd.DataFrame(flexibility, columns=['datetime', 'flexibility'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1h').mean()
        return total['flexibility'].values.tolist()

    def forecast_flexibility_saved_model(self):
        building_repo = BuildingRepository()
        consumption = pd.DataFrame(building_repo.get_totalpower_col())
        consumption = consumption.drop("_id", axis=1)
        forecast_adapter = ForecastAdapter()
        return forecast_adapter.forecast_day_consumption(consumption)

    def forecast_value(self):
        forecastvalue_list = self.building_repo.get_forecastvalue_col()
        df = pd.DataFrame(forecastvalue_list)

        df.drop('_id', inplace=True, axis=1)
        return df