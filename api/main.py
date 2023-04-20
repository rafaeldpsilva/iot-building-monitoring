import datetime
import random
import sys

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append('.')
import api.tokenManager as TM
import api.trust as trust_manager
from services.BuildingService import BuildingService
from services.TokenService import TokenService
from core.Core import Core
from utils import utils

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

@app.route('/', methods=['GET'])
@trust_manager.access_control
def home():
    return jsonify({'online': True})

@app.route('/tokens', methods=['GET'])
@TM.token_required
def get_token_list():
    token_service = TokenService()
    tokens = token_service.get_tokens()
    return jsonify({'tokens' : tokens})

@app.route('/tokens/generate', methods=['GET', 'POST'])
@TM.token_required
def generate_token():
    token = ''

    if request.method == 'POST':
        token = jwt.encode({
                'Name': request.get_json().get("name"),
                'List of Resources': request.get_json().get("listofresources"),
                'Data Aggregation': request.get_json().get("dataaggregation"),
                'Time Aggregation': request.get_json().get("timeaggregation"),
                'Embargo Period': request.get_json().get("embargo"),
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=request.get_json().get("exp"))
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
    return jsonify({'token' : token})

@app.route('/tokens/check', methods=['POST'])
@TM.token_required
def check_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.decode_token(token)

    return jsonify(token)

@app.route('/tokens/save', methods=['POST'])
@TM.token_required
def save_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.insert_token(token)

    return jsonify({'token' : token['token'] , 'datetime': token['datetime'] , 'active': token['active']})

@app.route('/tokens/revoke', methods=['POST'])
@TM.token_required
@trust_manager.admin
def revoke_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.revoke_token(token)

    return jsonify({'token' : token['token'] , 'datetime': token['datetime'] , 'active': token['active']})


@app.route('/historicold', methods=['GET'])
@TM.token_required
def historic_old():
    building_service = BuildingService()
    df = building_service.historic(TM)

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

@app.route('/historic', methods=['GET'])
@TM.token_required
def historic():
    building_service = BuildingService()
    historic_total = building_service.get_historic_total()
    return jsonify({'historic': historic_total})
    
@app.route('/iots', methods=['GET'])
@TM.token_required
def get_iots():
    building_service = BuildingService()
    iots = building_service.get_iots()
    return jsonify({'iots': iots})

@app.route('/energy/now', methods=['GET'])
@TM.token_required
def energy_now():
    consumption = cr.get_total_consumption()
    generation = cr.get_total_generation()

    return jsonify({'consumption': consumption, 'generation': generation, 'flexibility' : consumption * random.randrange(0,20) / 100})

@app.route('/energy/totalpower', methods=['GET'])
@TM.token_required
def energy_totalpower():
    data = cr.get_total_consumption()

    return jsonify({'totalpower': data})

@app.route('/energy/consumption', methods=['GET'])
@TM.token_required
def energy_consumption():
    consumption = cr.get_iot_consumption()
    json = []
    for i in range(len(consumption)):
        json.append({"resource": consumption[i][0],"values": consumption[i][1]})
    return jsonify(json)

@app.route('/energy/generation', methods=['GET'])
@TM.token_required
def energy_generation():
    generation = cr.get_iot_generation()
    json = []
    for i in range(len(generation)):
        json.append({"resource": generation[i][0],"values": generation[i][1]})
    return jsonify(json)

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
    iots = cr.get_forecasted_flexibility()
    building_service = BuildingService()
    [shift_kwh ,shift_hours] = building_service.get_shift_hours_kwh(iots)
    return jsonify({'shift_hours': shift_hours, 'shift_kwh': shift_kwh})

@app.route('/invitation', methods=['GET'])
@TM.token_required
def invitation():
    return jsonify({'response': "OK"})
    
@app.route('/audit/validate', methods=['GET'])
@TM.token_required
def audit_validate():
    return jsonify({'response': "OK"})

@app.route('/audit/check', methods=['GET'])
@TM.token_required
def audit_check():
    return jsonify({'response': "OK"})

if __name__ == "__main__":
    cr = Core()
    cr.daemon = True
    cr.start()

    config = utils.get_config()
    app.run(host='0.0.0.0', port=config['app']['port'])
    cr.join()
