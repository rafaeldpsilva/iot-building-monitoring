import datetime

import jwt

from database.TokenRepository import TokenRepository


class TokenService:
    def __init__(self):
        self.token_repo = TokenRepository()

    def get_tokens(self):
        tokens = self.token_repo.get_tokens()
        tokens_array = []
        for token in tokens:
            decoded = self.decode_token(token['token'])
            print(decoded)
            tokens_array.append(
                {'name': decoded['name'], 'list_of_resources': decoded['list_of_resources'], 'token': token['token'],
                 'expiration_time_minutes': decoded['expiration_time_minutes'], 'datetime': token['datetime']})
        return tokens_array

    def generate_token(self, secret_key, name, list_of_resources, data_aggregation, time_aggregation, embargo, exp):
        token = jwt.encode({
            'name': name,
            'list_of_resources': list_of_resources,
            'data_aggregation': data_aggregation,
            'time_aggregation': time_aggregation,
            'embargo_period': embargo,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=exp)
        },
            secret_key, algorithm="HS256"
        )
        return token

    def decode_token(self, token):
        decoded = jwt.decode(token, 'thisisthesecretkey', algorithms=["HS256"])
        return {'name': decoded['name'], 'list_of_resources': decoded['list_of_resources'], 'token': token,
                'expiration_time_minutes': decoded['exp'], 'data_aggregation': decoded['data_aggregation'],
                'time_aggregation': decoded['time_aggregation'], 'embargo_period': decoded['embargo_period']}

    def revoke_token(self, token):
        return self.token_repo.revoke_token(token)

    def insert_token(self, token):
        return self.token_repo.insert_token(token, str(datetime.datetime.now()))
