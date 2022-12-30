from flask import Flask, jsonify, request, make_response
import jwt 
import datetime
from functools import wraps
from pymongo import MongoClient
import json

dados = {}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

with open('./config/config.json') as config_file:
    data1 = json.load(config_file)

#connecting to database
client = MongoClient(str(data1['storage']['local']['server']) + ':' + str(data1['storage']['local']['port']))
db = client.Tokens_leftside
col = db.tokencol

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        global dados
        
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            for document in col.find():
                if token == document["token"]:
                    if document["active"] == False:
                        return jsonify({'message': 'Token was revoked'})
                    else:
                        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                        dados = data
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated