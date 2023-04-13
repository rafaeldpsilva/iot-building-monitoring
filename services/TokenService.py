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
            decoded = jwt.decode(token, 'thisisthesecretkey', algorithms=["HS256"])
            tokens_array.append({'name' : decoded['Name'],'List of Resources': decoded['List of Resources'],'token': token['token'], 'expiration_time_minutes': token['expiration_time_minutes'],'datetime': token['datetime']})
        return tokens_array
    
    def insert_token(self,token, exp):
        return self.token_repo.insert_token(token, exp, str(datetime.datetime.now()))