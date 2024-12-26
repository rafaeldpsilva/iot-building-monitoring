from database.BuildingRepository import BuildingRepository
from database.P2PRepository import P2PRepository
from database.FinancialRespository import FinancialRepository
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

    def get_p2p_intervals(self):
        today = datetime.now().replace(hour=0,minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        last_day = today - timedelta(days=1)
        repo = P2PRepository()
        p2p_transactions = repo.get_transactions(last_day, today)
        p2p_df = pd.DataFrame(p2p_transactions, columns=['datetime', 'quantity', 'cost'])
        p2p_df['datetime'] = pd.to_datetime(p2p_df['datetime'], format='%Y-%m-%dT%H:%M:%S.%fZ', dayfirst=True)
        p2p_df.set_index("datetime", inplace=True)
        p2p_df = p2p_df.resample('1h').mean()
        return {row['datetime']: row for row in p2p_df.reset_index().to_dict(orient='records')}

    
    def get_energy_from_retailer(self):
        total = self.get_intervals()
        p2p_dict = self.get_p2p_intervals()
        retailer = []
        for interval in total:
            datetime_interval = interval['datetime']
            p2p_sold = 0
            if datetime_interval in p2p_dict:
                p2p_entry = p2p_dict[datetime_interval]
                p2p_sold = p2p_entry['quantity']
                    
            retailer.append({"datetime": interval['datetime'], "retailer": interval['totalpower'] + p2p_sold - interval['totalgeneration']})
        #retailer = consumption + p2p_sold - generation - p2p_bought
        #retailer = consumption + (p2p_sold - p2p_bought) - generation 
        return retailer
    
    def get_self_consumption(self):
        total = self.get_intervals()
        p2p_dict = self.get_p2p_intervals()
        self_consumption = []
        for interval in total:
            datetime_interval = interval['datetime']
            p2p_sold = 0
            if datetime_interval in p2p_dict:
                p2p_entry = p2p_dict[datetime_interval]
                if p2p_entry['quantity'] < 0 and p2p_entry['cost'] > 0:  # P2P Sold
                    p2p_sold = abs(p2p_entry['quantity'])
    
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
                co2.append({"datetime": interval['datetime'], "co2_with_p2p": round(interval['retailer']/1000 * self.co2_constant,2)})
            else:
                co2.append({"datetime": interval['datetime'], "co2_with_p2p": 0})
        return co2
    
    def get_co2_without_p2p(self):
        total = self.get_intervals()
        co2 = []
        for interval in total:
            if interval['totalpower']- interval['totalgeneration'] > 0:
                co2.append({"datetime": interval['datetime'], "co2_without_p2p": round((interval['totalpower']- interval['totalgeneration'])/1000 * self.co2_constant,2)})
            else:
                co2.append({"datetime": interval['datetime'], "co2_without_p2p": 0})
        return co2
    
    def add_benefit(self, source, product, value):
        repo = FinancialRepository()
        repo.insert_benefit(source, product, value)
        repo.add_benefit(value)
    
    
    def get_benefit_historic(self):
        end = datetime.now().replace(day=1,hour=0,minute=0, second=0, microsecond=0)
        start = end - timedelta(days=2)
        start = start.replace(day=1)
        repo = FinancialRepository()
        return repo.get_benefit_historic(start, end)