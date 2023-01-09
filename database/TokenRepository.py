from pymongo import MongoClient
from utils import utils


class TokenRepository:
    def __init__(self):
        config = utils.get_config()

        client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        db1 = client.Tokens_leftside

        # criar a tabela
        self.tokensdb = db1.tokencol

    def get_leftside_tokencol(self):
        return self.tokensdb

    def insert_token(self, token, expiration_time_minutes, datetime):
        # inserir objeto em forma de dicionario em mongodb
        self.tokensdb.insert_one({"token": token,
                                  "expiration_time_minutes": expiration_time_minutes,
                                  "datetime": datetime,
                                  "active": True})
        return token