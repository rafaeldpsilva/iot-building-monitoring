import sys
from functools import wraps

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append('.')
from database.TokenRepository import TokenRepository

dados = {}
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisisthesecretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        global dados

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        token_repo = TokenRepository()
        col = token_repo.get_tokens()

        try:
            for document in col:
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
