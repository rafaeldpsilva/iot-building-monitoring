from datetime import datetime, timedelta
import random

import pandas as pd

from database.BuildingRepository import BuildingRepository
from modules.ForecastAdapter import ForecastAdapter


class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()

    def get_iots(self):
        return self.building_repo.get_iots()

    def get_shift_quantity(self,iots):
        shift_quantity = []
        for i in range(len(iots)):
            participant = []
            participant.append(random.randrange(1,3))
            shift_quantity.append(participant)
        return shift_quantity

    def get_shift_hours_kwh(self, iots):
        shift_quantity = self.get_shift_quantity(iots)
        shift_kwh = []
        shift_hours = []
        for i, device in enumerate(shift_quantity):
            for j, quantity in enumerate(device):
                iot_kwh = []
                iot_hour = []
                if quantity > 0:
                    iot_kwh.append(iots[i][1]/quantity)
                    iot_hour.append(random.randrange(0,23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                if quantity > 1:
                    iot_kwh.append(iots[i][1]/quantity)
                    iot_hour.append(random.randrange(0,23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                if quantity > 2:
                    iot_kwh.append(iots[i][1]/quantity)
                    iot_hour.append(random.randrange(0,23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                shift_kwh.append(iot_kwh)
                shift_hours.append(iot_hour)
        return [shift_kwh,shift_hours]

    def energy_consumption(self, TM, cr):
        consumption = []
        iots = cr.iots
        if TM.dados['Data Aggregation'] == 'individual':
            for resource in TM.dados['List of Resources']:
                for iot in iots:
                    if resource['text'] == iot.name:
                        if resource['text'] != 'Generation':
                            consumption.append({"resource": iot.name, "values": iot.get_power()})
                        else:
                            consumption.append({"resource": iot.name, "values": iot.get_generation()})
        else:
            consumption = {"resource": "end-user", "values": 0}
            for resource in TM.dados['List of Resources']:
                for iot in iots:
                    if resource['text'] == iot.name:
                        consumption['values'] += iot.get_power()
        return consumption

    def get_historic(self, start):
        total = self.building_repo.get_historic(start)
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
        return total.values.tolist()

    def get_historic_last_day(self):
        total = self.building_repo.get_historic(datetime.now() - timedelta(hours=24))
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
        
        total = total.dropna()
        
        total = total.values.tolist()
        total_power = []
        
        for row in total:
            iots = row[0]
            date = row[1]
            consumption = 0
            generation = 0
            flexibility = 0
            for iot in iots:
                for value in iot['values']:
                    if value['type'] == 'generation':
                        generation += value['values']
                    if value['type'] == 'power':
                        consumption += value['values']
                        flexibility += value['values'] * random.randrange(0,20) / 100

            total_power.append([date,consumption,generation,flexibility])
            
        total = pd.DataFrame(total_power, columns=['datetime', 'consumption','generation','flexibility'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1H').mean()
        total = total.tail(24)
        total['datetime'] = total.index
        total = total.values.tolist()
        return total


    def historic(self, TM):
        time = datetime.now() - timedelta(minutes=180)
        timeemb = datetime.now() - timedelta(minutes=int(TM.dados['Embargo Period']))

        indexArray = []
        dataArray = []
        columns = []
        if TM.dados['Data Aggregation'] == 'sum':
            columns.append("end-user")

        getIndex = True
        iots_reading = []
        for i in TM.dados['List of Resources']:
            iots_reading = self.building_repo.get_iots_reading_col(time, timeemb)
            if TM.dados['Data Aggregation'] == 'individual':
                columns.append(i['text'])
            index = 0
            for entry in iots_reading:
                if getIndex:
                    indexArray.append(datetime.strptime(entry["datetime"][:19], "%Y-%m-%d %H:%M:%S"))
                    dataArray.append([])
                    if TM.dados['Data Aggregation'] == 'sum':
                        dataArray[index].append(0)
                if TM.dados['Data Aggregation'] == 'individual':
                    dataArray[index].append(get_value(entry['iot_values'], 'power'))
                else:
                    dataArray[index][0] += get_value(entry['iot_values'], 'power')
                index += 1
            if getIndex:
                getIndex = False

        df = pd.DataFrame(dataArray, index=indexArray, columns=columns)

        if TM.dados["Time Aggregation"] == "5minutes":
            df=df.groupby(df.index.floor('5T')).mean()
        elif TM.dados["Time Aggregation"] == "15minutes":
            df=df.groupby(df.index.floor('15T')).mean()
        elif TM.dados["Time Aggregation"] == "60minutes":
            df=df.groupby(df.index.floor('60T')).mean()

        return df

    def forecast_consumption(self):
        building_repo = BuildingRepository()
        consumption = pd.DataFrame(building_repo.get_totalpower_col())
        consumption = consumption.drop("_id", axis=1)
        forecast_adapter = ForecastAdapter()
        return forecast_adapter.forecast_day_consumption(consumption)

    def forecast_flexibility(self):
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

def get_value(array, type):
    for value in array:
        if value['type'] == type:
            return (value['values'])
    return -1
