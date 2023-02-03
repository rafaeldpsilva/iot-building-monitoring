import sys
import datetime
import random
from flask_cors import CORS
import jwt
from flask import Flask, jsonify, request
sys.path.append('.')
from services.BuildingService import BuildingService
import api.tokenManager as TM
from database.TokenRepository import TokenRepository
from core.Core import Core
from utils import utils

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


#? PORQUE GET E POST

@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({'online': True})


@app.route('/building/energy', methods=['GET', 'POST'])
@TM.token_required
def protected_energy():
    building_service = BuildingService()
    consumption = building_service.protected_energy(TM, cr)

    return jsonify({'consumption': consumption})

#! Deveria ser divido entre GET REQUEST E POST REQUEST
@app.route('/generate_token', methods=['GET', 'POST'])
def generate_token():
    token = ''

    if request.method == 'POST':
        token = jwt.encode({
                'Name': request.get_json().get("name"),
                'List of Resources': request.get_json().get("listofresources"),
                'Data Aggregation': request.get_json().get("dataaggregation"),
                'Time Aggregation': request.get_json().get("timeaggregation"),
                'Embargo Period': request.get_json().get("embargo"),
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=request.get_json().get("exp")) #? exp é expiration
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )

    token_repo = TokenRepository()

    token = token_repo.insert_token(token, request.get_json().get("exp"), datetime.datetime.now())

    return jsonify({'token': token})


@app.route('/building/historic', methods=['GET', 'POST'])
@TM.token_required
def protected_historic():
    building_service = BuildingService()
    df = building_service.protected_historic(TM)

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )


@app.route('/building/rightside/totalpower', methods=['GET', 'POST'])
@TM.token_required
def rightside_totalpower():
    data = cr.get_total_consumption()

    return jsonify({'totalpower': data})


@app.route('/building/rightside/generation', methods=['GET', 'POST'])
@TM.token_required
def rightside_generation():
    data = 'NULL'

    for iot in cr.iots:
        data = iot.get_generation()

    return jsonify({'Generation': data})

@app.route('/building/flexibility', methods=['GET'])
@TM.token_required
def get_flexibility():
    flexibility = cr.get_total_consumption() * random.randrange(0,0.2)
    return jsonify({'flexibility': flexibility})

@app.route('/building/correlations', methods=['GET', 'POST'])
def correlations():
    return


@app.route('/building/forecast', methods=['GET'])
@TM.token_required
def forecast():
    building_service = BuildingService()
    df = building_service.forecast()

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    cr = Core()
    cr.daemon = True
    cr.start()

    config = utils.get_config()
    app.run(host='0.0.0.0', port=config['app']['port'])
    cr.join()
