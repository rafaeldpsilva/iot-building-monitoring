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


@app.route('/historic', methods=['GET', 'POST'])
@TM.token_required
def historic():
    building_service = BuildingService()
    df = building_service.historic(TM)

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

@app.route('/energy/now', methods=['GET'])
@TM.token_required
def energy_now():
    consumption = cr.get_total_consumption()
    generation = 'NULL'
    for iot in cr.iots:
        generation = iot.get_generation()

    return jsonify({'consumption': consumption, 'generation': generation, 'flexibility' : consumption * random.randrange(0,20) / 100})

@app.route('/energy/totalpower', methods=['GET', 'POST'])
@TM.token_required
def energy_totalpower():
    data = cr.get_total_consumption()

    return jsonify({'totalpower': data})

@app.route('/energy/consumption', methods=['GET', 'POST'])
@TM.token_required
def energy_consumption():
    building_service = BuildingService()
    consumption = building_service.energy_consumption(TM, cr)

    return jsonify({'consumption': consumption})

@app.route('/energy/generation', methods=['GET', 'POST'])
@TM.token_required
def energy_generation():
    data = 'NULL'

    for iot in cr.iots:
        data = iot.get_generation()

    return jsonify({'generation': data})

@app.route('/energy/flexibility', methods=['GET'])
@TM.token_required
def energy_flexibility():
    flexibility = cr.get_total_consumption() * random.randrange(0,20)/100
    return jsonify({'flexibility': flexibility})

@app.route('/correlations', methods=['GET', 'POST'])
def correlations():
    return

@app.route('/forecast/consumption', methods=['GET'])
@TM.token_required
def forecast_consumption():
    building_service = BuildingService()
    forecasted_consumption = building_service.forecast_consumption().numpy().tolist()

    consumption = []
    for val in forecasted_consumption:
        consumption.append(val * random.randrange(0,20)/100)

    return jsonify({'forecasted_consumption': consumption})

@app.route('/forecast/flexibility', methods=['GET'])
@TM.token_required
def forecast_flexibility():
    flexibility = cr.get_forecasted_flexibility()

    # building_service = BuildingService()
    # forecasted_flexibility = building_service.forecast_consumption().numpy().tolist()

    # flexibility = []
    # for val in forecasted_flexibility:
    #     flexibility.append(val * random.randrange(0,20)/100)

    return jsonify({'forecasted_flexibility': flexibility})

@app.route('/forecast', methods=['GET'])
@TM.token_required
def forecast_value():
    building_service = BuildingService()
    df = building_service.forecast_value()

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

@app.route('/shifting', methods=['GET'])
@TM.token_required
def get_shifting():
    iots = cr.get_iots()
    building_service = BuildingService()
    [shift_kwh ,shift_hours] = building_service.get_shift_hours_kwh(iots)
    return jsonify({'shift_hours': shift_hours, 'shift_kwh': shift_kwh})

@app.route('/invitation', methods=['GET'])
@TM.token_required
def invitation():
    return jsonify({'response': "OK"})

if __name__ == "__main__":
    cr = Core()
    cr.daemon = True
    cr.start()

    config = utils.get_config()
    app.run(host='0.0.0.0', port=config['app']['port'])
    cr.join()
