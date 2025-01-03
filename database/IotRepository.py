from datetime import datetime

from pymongo import MongoClient

from utils import utils


class IotRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.IOTS_READING = self.config['storage']['local']['iots_reading']
        self.INSTRUCTIONS = self.config['storage']['local']['instructions']

    def get_iots(self):
        iots = []
        for iot in self.config['resources']['iots']:
            iots.append(iot)
        return iots

    def insert_iots(self, iots, datetime):
        try:
            iots_save = {"iots": iots, "datetime": datetime}
            client = MongoClient(f"{self.server}:{self.port}")
            client[self.IOTS_READING[0]][self.IOTS_READING[1]].insert_one(iots_save)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

    def get_historic_by_interval(self, start: datetime, end: datetime):
        client = MongoClient(f"{self.server}:{self.port}")
        historic = list(
            client[self.IOTS_READING[0]][self.IOTS_READING[1]].find({'datetime': {'$gt': start, '$lt': end}}))
        client.close()
        return historic

    def update_instructions(self, instructions):
        try:
            iots_save = {"instructions": instructions}
            client = MongoClient(f"{self.server}:{self.port}")
            client[self.INSTRUCTIONS[0]][self.INSTRUCTIONS[1]].update_one({}, {"$set": iots_save}, upsert=True)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()
    
    def get_instructions(self):
        try:
            client = MongoClient(f"{self.server}:{self.port}")
            collection = client[self.INSTRUCTIONS[0]][self.INSTRUCTIONS[1]]
            result = collection.find_one({})
            
            return result["instructions"] if result else None
        
        except Exception as e:
            print("An exception occurred ::", e)
            return None
        finally:
            client.close()
            
    def change_dr_enable(self, iot_name, enable):
        raise RuntimeError('DEPRECATED: Change Dr enabling is not possible on this version')
        """success = False
        for iot in self.config['resources']['iots']:
            if iot['name'] == iot_name:
                iot['control']['demandresponse'] = enable
                success = True
        if success:
            utils.save_config(self.config) """
