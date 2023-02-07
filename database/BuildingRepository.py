from pymongo import MongoClient
from utils import utils


class BuildingRepository:
    def __init__(self):
        self.config = utils.get_config()

        #self.client = MongoClient(
        #    str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.IOTS_READING = self.config['storage']['local']['iots_reading']
        self.FORECAST = self.config['storage']['local']['forecast']
        self.TOTALPOWER = self.config['storage']['local']['totalpower']

    def client(self):
        return MongoClient(self.server + ':' + self.port)

    def get_iots_reading_col(self, name, time, time_emb):
        client = self.client()
        building_iot_reading = list(client[self.IOTS_READING[0]][self.IOTS_READING[1]].find({"name": name, 'datetime': { '$gt': str(time), '$lt' : str(time_emb)} } ))
        client.close()
        return building_iot_reading

    def get_forecastvalue_col(self):
        #? devia haver class forecastRepo
        client = self.client()
        forecastvalue = list(client.ForecastDay.forecastvalue.find())
        client.close()
        return forecastvalue

    def get_totalpower_col(self):
        client = self.client()
        building_totalpower = list(client[self.TOTALPOWER[0]][self.TOTALPOWER[1]].find())
        client.close()
        return building_totalpower

    def insert_totalpower(self, totalpower, datetime):
        try:
            totalpower = {"totalpower": totalpower, "datetime": datetime}
            client = self.client()
            client[self.TOTALPOWER[0]][self.TOTALPOWER[1]].insert_one(totalpower)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nTotalPower\n',totalpower)


    def insert_iot(self, name, type, iot_values, datetime):
        try:
            iot = {"name": name, "type": type, "iot_values": iot_values, "datetime": datetime}
            client = self.client()
            client[self.IOTS_READING[0]][self.IOTS_READING[1]].insert_one(iot)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nIoT\n',iot)

    def insert_forecast(self, forecast_power, datetime):
        try:
            forecast = {"forecast_power": forecast_power, "datetime": datetime}
            client = self.client()
            client[self.FORECAST[0]][self.FORECAST[1]].insert_one(forecast)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()
        
        if self.config['app']['monitoring']:
            print('\nForecast\n',forecast)

    def insert_forecastday(self, iat, datetime):
        try:
            forecastday = {"forecast_power": {"0": str(iat[0, 0]),
                                                  "1": str(iat[1, 0]),
                                                  "2": str(iat[2, 0]),
                                                  "3": str(iat[3, 0]),
                                                  "4": str(iat[4, 0]),
                                                  "5": str(iat[5, 0]),
                                                  "6": str(iat[6, 0]),
                                                  "7": str(iat[7, 0]),
                                                  "8": str(iat[8, 0]),
                                                  "9": str(iat[9, 0]),
                                                  "10": str(iat[10, 0]),
                                                  "11": str(iat[11, 0]),
                                                  "12": str(iat[12, 0]),
                                                  "13": str(iat[13, 0]),
                                                  "14": str(iat[14, 0]),
                                                  "15": str(iat[15, 0]),
                                                  "16": str(iat[16, 0]),
                                                  "17": str(iat[17, 0]),
                                                  "18": str(iat[18, 0]),
                                                  "19": str(iat[19, 0]),
                                                  "20": str(iat[20, 0]),
                                                  "21": str(iat[21, 0]),
                                                  "22": str(iat[22, 0]),
                                                  "23": str(iat[23, 0])},
                               "datetime": datetime}
            client = self.client()
            client.ForecastDay.forecastvalue.insert_one(forecastday)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nForecastDay\n',forecastday)
