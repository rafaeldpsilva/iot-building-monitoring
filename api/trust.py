from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS

from services.TokenService import TokenService

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisisthesecretkey'


def aggregated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        token_service = TokenService()
        decoded = token_service.decode_token(token)

        access = False
        for access_resource in decoded['list_of_resources']:
            if access_resource == 'aggregated':
                access = True

        if not access:
            return jsonify({'message': 'Access not allowed'})
        return f(*args, **kwargs)

    return decorated


def discrete(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        token_service = TokenService()
        decoded = token_service.decode_token(token)
        access = False
        for access_resource in decoded['list_of_resources']:
            if access_resource == 'discrete':
                access = True

        if not access:
            return jsonify({'message': 'Access not allowed'})

        return f(*args, **kwargs)

    return decorated


def admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        token_service = TokenService()
        decoded = token_service.decode_token(token)
        access = False
        for access_resource in decoded['list_of_resources']:
            if access_resource == 'admin':
                access = True

        if not access:
            return jsonify({'message': 'Access not allowed'})
        return f(*args, **kwargs)

    return decorated


def community_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur
        token_service = TokenService()
        decoded = token_service.decode_token(token)
        access = False
        for access_resource in decoded['list_of_resources']:
            if access_resource == 'community_manager':
                access = True

        if not access:
            return jsonify({'message': 'Access not allowed'})

        return f(*args, **kwargs)

    return decorated
