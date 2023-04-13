import datetime
from database.TokenRepository import TokenRepository
import jwt

class TokenService:
    def __init__(self):
        self.token_repo = TokenRepository()
    
    def get_tokens(self):
        tokens = self.token_repo.get_tokens()
        tokens_array = []
        for token in tokens:
            decoded = jwt.decode(token['token'], 'thisisthesecretkey', algorithms=["HS256"])
            tokens_array.append({'name' : decoded['Name'],'list_of_resources': decoded['List of Resources'],'token': token['token'], 'expiration_time_minutes': token['expiration_time_minutes'],'datetime': token['datetime']})
        return tokens_array
    
    def decode_token(self, token):
        decoded = jwt.decode(token['token'], 'thisisthesecretkey', algorithms=["HS256"])
        return {'name' : decoded['Name'],'list_of_resources': decoded['List of Resources'],'token': token['token'], 'expiration_time_minutes': token['expiration_time_minutes'],'datetime': token['datetime']}
        
    def insert_token(self,token):
        return self.token_repo.insert_token(token, str(datetime.datetime.now()))