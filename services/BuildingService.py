import random
from datetime import datetime, timedelta

import pandas as pd

from database.BuildingRepository import BuildingRepository
from modules.ForecastAdapter import ForecastAdapter


class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()

    def get_shift_quantity(self, iots):
        shift_quantity = []
        for i in range(len(iots)):
            participant = []
            participant.append(random.randrange(1, 3))
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
                    iot_kwh.append(iots[i][1] / quantity)
                    iot_hour.append(random.randrange(0, 23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                if quantity > 1:
                    iot_kwh.append(iots[i][1] / quantity)
                    iot_hour.append(random.randrange(0, 23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                if quantity > 2:
                    iot_kwh.append(iots[i][1] / quantity)
                    iot_hour.append(random.randrange(0, 23))
                else:
                    iot_kwh.append(0)
                    iot_hour.append(0)
                shift_kwh.append(iot_kwh)
                shift_hours.append(iot_hour)
        return [shift_kwh, shift_hours]

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

    def get_mean_values(self, start):
        historic = self.building_repo.get_historic(start)
        instants = 0
        consumption = []
        generation = []
        for instant in historic:
            instants += 1
            for iot in instant['iots']:
                for value in iot['values']:
                    if 'values' in value:
                        if value['type'] == "power":
                            consumption.append([iot['name'], value['values']])

                        if iot['type'] == "generation":
                            generation.append([iot['name'], value['values']])
        if len(consumption) != 0:
            return consumption, generation, instants
        else:
            return [0], [0], 1

    def get_historic(self, start):
        total = self.building_repo.get_historic(start)
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
        return total.values.tolist()

    def save_last_hour(self):
        end_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        start_hour = end_hour - timedelta(hours=1)
        last_hour = self.building_repo.get_historic_interval(start_hour, end_hour)
        last_hour = pd.DataFrame(last_hour)
        last_hour = last_hour.drop(["_id"], axis=1)

        last_hour = last_hour.dropna()

        last_hour = last_hour.values.tolist()
        total_power = []

        for row in last_hour:
            iots = row[0]
            date = row[1]
            consumption = 0
            generation = 0
            flexibility = 0
            for iot in iots:
                for value in iot['values']:
                    if 'values' in value:
                        if value['type'] == 'generation':
                            generation += value['values']
                        if value['type'] == 'power':
                            consumption += value['values']
                            flexibility += value['values'] * random.randrange(0, 20) / 100

            total_power.append([date, consumption, generation, flexibility])

        total = pd.DataFrame(total_power, columns=['datetime', 'consumption', 'generation', 'flexibility'])
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1h').mean()
        total = total.values.tolist()
        self.building_repo.insert_hour(start_hour, total[0][0], total[0][1], total[0][2])

    def get_historic_last_day_by_hour(self):
        total = self.building_repo.get_historic_hour(
            datetime.strftime(datetime.now() - timedelta(hours=24), "%Y-%m-%d %H:%M:%S"))
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
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
            df = df.groupby(df.index.floor('5T')).mean()
        elif TM.dados["Time Aggregation"] == "15minutes":
            df = df.groupby(df.index.floor('15T')).mean()
        elif TM.dados["Time Aggregation"] == "60minutes":
            df = df.groupby(df.index.floor('60T')).mean()

        return df

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

    def forecast_consumption_saved_model(self):
        forecast_adapter = ForecastAdapter()
        return forecast_adapter.forecast_saved_model()

    def forecast_generation_saved_model(self):
        forecast_adapter = ForecastAdapter()
        return forecast_adapter.forecast_generation_saved_model()

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
