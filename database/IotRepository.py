from datetime import datetime

from pymongo import MongoClient

from utils import utils


class IotRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.IOTS_READING = self.config['storage']['local']['iots_reading']

    def get_iots(self):
        iots = []
        for iot in self.config['resources']['iots']:
            iots.append(iot)
        return iots

    def insert_iots(self, iots, datetime):
        try:
            iots_save = {"iots": iots, "datetime": datetime}
            client = MongoClient(self.server + ':' + self.port)
            client[self.IOTS_READING[0]][self.IOTS_READING[1]].insert_one(iots_save)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nIoTS\n', iots_save)

    def get_historic_by_interval(self, start: datetime, end: datetime):
        client = MongoClient(self.server + ':' + self.port)
        historic = list(
            client[self.IOTS_READING[0]][self.IOTS_READING[1]].find({'datetime': {'$gt': start, '$lt': end}}))
        client.close()
        return historic

    def change_dr_enable(self, iot_name, enable):
        raise RuntimeError('DEPRECATED: Change Dr enabling is not possible on this version')
        """success = False
        for iot in self.config['resources']['iots']:
            if iot['name'] == iot_name:
                iot['control']['demandresponse'] = enable
                success = True
        if success:
            utils.save_config(self.config) """
