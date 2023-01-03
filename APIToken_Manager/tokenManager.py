from functools import wraps

import jwt
from flask import Flask, jsonify, request

from APIToken_Manager.TokenRepository import TokenRepository

dados = {}
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

token_repo = TokenRepository()
col = token_repo.get_leftside_tokencol()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        global dados

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            for document in col.find():
                if token == document["token"]:
                    if not document["active"]:
                        return jsonify({'message': 'Token was revoked'})
                    else:
                        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                        dados = data
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated
