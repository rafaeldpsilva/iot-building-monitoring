from pymongo import MongoClient

from utils import utils


class DivisionRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.DIVISIONS = self.config['storage']['local']['divisions']
        self.CONFIG = self.config['storage']['local']['config']

    def get_divisions(self):
        client = MongoClient(self.server + ':' + self.port)
        divisions = list(client[self.DIVISIONS[0]][self.DIVISIONS[1]].find())
        client.close()
        return divisions

    def insert_division(self, name, iots):
        try:
            division_save = {"name": name, "iots": iots}
            client = MongoClient(self.server + ':' + self.port)
            client[self.DIVISIONS[0]][self.DIVISIONS[1]].insert_one(division_save)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nDivision\n', division_save)

    def set_ac_status_model_configuration(self, historic_interval, considered_iots, outside_temperature_colname,
                                          temperature_colname, humidity_colname, light_colname):
        try:
            model_configuration = {"config": "ac_status", "historic_interval": historic_interval,
                                   "considered_iots": considered_iots,
                                   "colnames": {"outside_temperature": outside_temperature_colname, "temperature":
                                       temperature_colname, "humidity": humidity_colname, "light": light_colname}}
            client = MongoClient(self.server + ':' + self.port)
            client[self.CONFIG[0]][self.CONFIG[1]].insert_one(model_configuration)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nAC Status Model Configuration\n', model_configuration)

    def get_ac_status_configuration(self):
        client = MongoClient(self.server + ':' + self.port)
        divisions = list(client[self.CONFIG[0]][self.CONFIG[1]].find({"config": "ac_status"}))
        client.close()
        return divisions[0]
