from pymongo import MongoClient

from utils import utils


class DivisionRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.DIVISIONS = self.config['storage']['local']['divisions']

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
