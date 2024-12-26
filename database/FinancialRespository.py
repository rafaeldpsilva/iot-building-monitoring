from datetime import datetime

from pymongo import MongoClient

from utils import utils


class FinancialRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.BALANCE = self.config['storage']['local']['balance']
        self.BENEFIT = self.config['storage']['local']['benefit']

    def insert_benefit(self, source, product, value):
        try:
            benefit = { "datetime": datetime.now(), "source": source, "product": product, "value": value}
            client = MongoClient(self.server + ':' + self.port)
            client[self.BENEFIT[0]][self.BENEFIT[1]].insert_one(benefit)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

    def add_benefit(self, value):
        client = MongoClient(self.server + ':' + self.port)
        balance = list(client[self.BALANCE[0]][self.BALANCE[1]].find().sort("datetime", -1).limit(1))
        client.close()
        if balance[0]['balance'] == []:
            new_balance = value
        else:
            new_balance = balance[0]['balance'] + value
        try:
            json = {"datetime": datetime.now(), "balance": new_balance}
            client = MongoClient(self.server + ':' + self.port)
            client[self.BALANCE[0]][self.BALANCE[1]].insert_one(json)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

    def get_benefit_historic(self, start, end):
        client = MongoClient(self.server + ':' + self.port)
        benefits = list(client[self.BENEFIT[0]][self.BENEFIT[1]].find({'datetime': {'$gt': start, '$lt': end}}))
        client.close()
        return benefits
