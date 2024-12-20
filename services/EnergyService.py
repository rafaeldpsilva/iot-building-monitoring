from database.BuildingRepository import BuildingRepository
from datetime import datetime, timedelta
import pandas as pd


class EnergyService:
    def __init__(self):
        self.co2_constant = 20

    def get_intervals(self):
        today = datetime.now().replace(hour=0,minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        last_day = today - timedelta(days=1)
        repo = BuildingRepository()
        totalpower = repo.get_power_historic_interval(last_day, today)
        total = pd.DataFrame(totalpower, columns=['totalpower', 'totalgeneration', 'datetime'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1h').mean()
        total['datetime'] = total.index
        return total.to_dict(orient='records')

    def get_energy_from_retailer(self):
        total = self.get_intervals()
        retailer = []
        for interval in total:
            retailer.append({"datetime": interval['datetime'], "retailer": interval['totalpower'] - interval['totalgeneration']})
        #retailer = consumption + p2p_sold - generation - p2p_bought
        return retailer
    
    def get_self_consumption(self):
        total = self.get_intervals()
        self_consumption = []
        for interval in total:
            p2p_sold = 0
            if interval['totalgeneration'] - p2p_sold < interval['totalpower']:
                self_consumption.append({"datetime": interval['datetime'], "self_consumption": interval['totalgeneration'] - p2p_sold})
            else:
                self_consumption.append({"datetime": interval['datetime'], "self_consumption": interval['totalpower']})
        return self_consumption

    def get_co2_with_p2p(self):
        retailer = self.get_energy_from_retailer()
        co2 = []
        for interval in retailer:  
            if interval['retailer'] > 0:
                co2.append({"datetime": interval['datetime'], "co2_with_p2p": interval['retailer']/1000 * self.co2_constant})
            else:
                co2.append({"datetime": interval['datetime'], "co2_with_p2p": 0})
        return co2
    
    def get_co2_without_p2p(self):
        total = self.get_intervals()
        co2 = []
        for interval in total:  
            if interval['totalpower']- interval['totalgeneration'] > 0:
                co2.append({"datetime": interval['datetime'], "co2_without_p2p": (interval['totalpower']- interval['totalgeneration']) * self.co2_constant})
            else:
                co2.append({"datetime": interval['datetime'], "co2_without_p2p": 0})
        return co2