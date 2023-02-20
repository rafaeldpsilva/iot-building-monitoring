import datetime
import pymongo
import pandas as pd
from database.BuildingRepository import BuildingRepository
class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()

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

    def historic(self, TM):
        time = datetime.datetime.now() - datetime.timedelta(minutes=180)
        timeemb = datetime.datetime.now() - datetime.timedelta(minutes=int(TM.dados['Embargo Period']))

        indexArray = []
        dataArray = []
        columns = []
        if TM.dados['Data Aggregation'] == 'sum':
            columns.append("end-user")

        getIndex = True
        for i in TM.dados['List of Resources']:
            x = self.building_repo.get_iots_reading_col(i['text'],time, timeemb)
            y = list(x)
            if TM.dados['Data Aggregation'] == 'individual':        #? PARA QUE SERVE
                columns.append(i['text'])
            index = 0
            for entry in y:
                if getIndex:
                    indexArray.append(datetime.datetime.strptime(entry["datetime"][:19], "%Y-%m-%d %H:%M:%S"))
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
        forecast_adapter = ForecastAdapter()
        df = forecast_adapter.forecast_day_consumption(consumption)
        return df

    def forecast_value(self):
        forecastvalue_list = self.building_repo.get_forecastvalue_col()
        df = pd.DataFrame(forecastvalue_list)

        df.drop('_id', inplace=True, axis=1)
        # df = df.iloc[1: , :]
        # print(df)
        # df.drop('0', inplace=True, axis=1)
        # df_n = df.set_index('datetime')
        # reversed_df = df_n.iloc[::-1]

        return df
def get_value(array, type):
    for value in array:
        if value['type'] == type:
            # print(value)
            return (value['values'])
    return -1
