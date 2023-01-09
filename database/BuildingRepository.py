from pymongo import MongoClient
from utils import utils


class BuildingRepository:
    def __init__(self):
        config = utils.get_config()

        self.client = MongoClient(
            str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))

    def get_iots_reading_col(self):
        db = self.client.BuildingRightSide
        return db.iots_reading

    def get_forecastvalue_col(self):
        #? devia haver class forecastRepo
        db = self.client.ForecastDay
        return db.forecastvalue

    def get_powerrightside_col(self):
        #? devia haver class forecastRepo
        db = self.client.TotalPower
        return db.powerrightside

    def insert_totalpower(self, totalpower, datetime):
        db = self.client.TotalPower
        # criar a tabela
        total = db.powerrightside
        # inserir objeto em forma de dicionario em mongodb
        total.insert_one({"totalpower": totalpower, "datetime": datetime})

    def insert_iot(self, name, type, iot_values, datetime):
        iots = self.get_iots_reading_col()
        iots.insert_one({"name": name, "type": type, "iot_values": iot_values, "datetime": datetime})

    def insert_forecast_rightside(self, forecast_power, datetime):
        db = self.client.Forecast
        forecastdb = db.forecastvaluerightside
        forecastdb.insert_one({"forecast_power": forecast_power, "datetime": datetime})

    def insert_forecastday(self, iat, datetime):
        db = self.client.ForecastDay
        forecastdb = db.forecastvalue

        # inserir objeto em forma de dicionario em mongodb
        forecastdb.insert_one({"forecast_power": {"0": str(iat[0, 0]),
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
                               "datetime": datetime})

