from pymongo import MongoClient
import json

class BuildingRepository:
    def __init__(self):
        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        self.client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        db1 = client.BuildingRightSide
        
        self.iots_reading_col = db.iots_reading

    def get_iots_reading_col():
        return self.iots_reading_col
    
    def get_forecastvalue_col():
        #? devia haver class forecastRepo
        db = self.client.ForecastDay
        return db.forecastvalue

    def get_powerrightside_col():
        #? devia haver class forecastRepo
        db = self.client.TotalPower
        return db.powerrightside
        
