from pymongo import MongoClient
import json

class BuildingRepository:
    def __init__(self):
        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        self.client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))

    def get_iots_reading_col():
        db1 = client.BuildingRightSide        
        return db.iots_reading
    
    def get_forecastvalue_col():
        #? devia haver class forecastRepo
        db = self.client.ForecastDay
        return db.forecastvalue

    def get_powerrightside_col():
        #? devia haver class forecastRepo
        db = self.client.TotalPower
        return db.powerrightside

    def insert_totalpower(totalpower, datetime):
        db = self.client.TotalPower
        #criar a tabela
        total = db.powerrightside
        #inserir objeto em forma de dicionario em mongodb
        total.insert_one({"totalpower": totalpower, 
                    "datetime" : datetime})
    
    def insert_iot(name,type,iot_values,datetime):
        iots = self.get_iots_reading_col()
        iots.insert_one({"name": name, 
                    "type": type, 
                    "iot_values" : values, 
                    "datetime" : datetime})
        
