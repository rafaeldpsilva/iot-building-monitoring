from pymongo import MongoClient
from utils import utils


class TokenRepository:
    def __init__(self):
        config = utils.get_config()

        self.server = str(config['storage']['local']['server'])
        self.port = str(config['storage']['local']['port'])

        # criar a tabela
        self.TOKEN = config['storage']['local']['token']
        
    def client(self):
        return MongoClient(self.server + ':' + self.port)

    def get_tokencol(self):
        client = self.client()
        tokenscol = list(client[self.TOKEN[0]][self.TOKEN[1]].find())
        client.close()
        return tokenscol

    def insert_token(self, token, expiration_time_minutes, datetime):
        try:
            client = self.client()
            # inserir objeto em forma de dicionario em mongodb
            client[self.TOKEN[0]][self.TOKEN[1]].insert_one({"token": token,
                                    "expiration_time_minutes": expiration_time_minutes,
                                    "datetime": datetime,
                                    "active": True})
            client.close()
        except ConnectionError as exc:
            raise RuntimeError('Failed to insert token') from exc
        return token
