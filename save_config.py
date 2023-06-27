from pymongo import MongoClient, DESCENDING
from utils import utils
config = utils.get_config()
db = config['storage']['local']['database']
server = str(config['storage']['local']['server'])
port = str(config['storage']['local']['port'])
def insert_config():
    try:
        client = MongoClient(server + ':' + port)
        client[db]['config'].insert_one(config)
    except Exception as e:
        print("An exception occurred ::", e)
    finally:
        client.close()

    if config['app']['monitoring']:
        print('\nConfig\n',config)
        
insert_config()
