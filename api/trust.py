import jwt
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def access_control(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
    
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        data_exp = datetime.strftime(data['exp'])
        if data_exp > datetime.now():
            return jsonify({'message': 'Token has expired'})
    

        return f(*args, **kwargs)

    return decorated