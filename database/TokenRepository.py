from pymongo import MongoClient
from utils import utils


class TokenRepository:
    def __init__(self):
        self.config = utils.get_config()

        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])

        # criar a tabela
        self.TOKEN = self.config['storage']['local']['token']
        
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
            token = {"token": token,
                        "expiration_time_minutes": expiration_time_minutes,
                        "datetime": datetime,
                        "active": True}
            client[self.TOKEN[0]][self.TOKEN[1]].insert_one(token)
            client.close()

            if self.config['app']['monitoring']:
                print('\nToken\n',token)

        except ConnectionError as exc:
            raise RuntimeError('Failed to insert token') from exc
        return token
