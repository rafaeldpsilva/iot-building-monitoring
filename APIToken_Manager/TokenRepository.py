from pymongo import MongoClient
import json

class TokenRepository:
    def __init__(self):
        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        db1 = client.Tokens_leftside
            
        #criar a tabela
        self.tokensdb = db1.tokencol

    def get_leftside_tokencol():
        return self.tokensdb

    def insert_token(token, expiration_time_minutes, datetime):
        #inserir objeto em forma de dicionario em mongodb
        self.tokensdb.insert_one({"token": token,
                    "expiration_time_minutes" : expiration_time_minutes,
                    "datetime": datetime,
                    "active": True})
        return token