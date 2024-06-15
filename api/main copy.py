import random
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append('.')
import api.tokenManager as TM
import api.trust as trust_manager
from services.IotService import IotService
from services.DivisionService import DivisionService
from services.BatteryService import BatteryService
from services.BuildingService import BuildingService
from services.TokenService import TokenService
from services.DemandResponseService import DemandResponseService
from core.Core import Core
from utils import utils
from modules.RenDatahub import get_production_breakdown

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


@app.route('/', methods=['GET'])
def home():
    return jsonify({'online': True})

@app.route('/overview', methods=['GET'])
@TM.token_required
@trust_manager.aggregated
def overview():
    building_service = BuildingService()
    historic_overview = building_service.get_historic_overview()
    forecast = building_service.forecast_consumption()
    return jsonify({'historic': historic_overview, 'forecast': forecast})

@app.route('/historic', methods=['GET'])
@TM.token_required
@trust_manager.aggregated
def historic():
    building_service = BuildingService()
    historic_last_day = building_service.get_historic_last_day_by_hour()
    return jsonify({'historic': historic_last_day})

#!TODO USE TOTALPOWER ON THIS INSTEAD OF IOTREADINGS
@app.route('/historic/interval', methods=['POST'])
@TM.token_required
@trust_manager.discrete
def energy_consumption_interval():
    json = request.get_json()
    start = json['start']
    building_service = BuildingService()
    consumption, generation, instants = building_service.get_mean_values(start)
    return jsonify({'consumption': consumption, 'generation': generation, "instants": instants})


@app.route('/iots', methods=['GET'])
@TM.token_required
@trust_manager.discrete
def get_iots():
    iot_service = IotService()
    iots = iot_service.get_iots()
    return jsonify({'iots': iots})

@app.route('/iot/historic', methods=['POST'])
@TM.token_required
def get_iot_historic():
    json = request.get_json()
    iot = json['iot']
    iot_service = IotService()
    historic = iot_service.get_iot_historic(iot)
    return jsonify({'historic': historic})

@app.route('/energy/now', methods=['GET'])
@TM.token_required
@trust_manager.aggregated
def energy_now():
    consumption = cr.get_total_consumption()
    generation = cr.get_total_generation()

    return jsonify({'consumption': consumption, 'generation': generation,
                    'flexibility': consumption * random.randrange(0, 20) / 100})

@app.route('/energy/totalpower', methods=['GET'])
@TM.token_required
@trust_manager.aggregated
def energy_totalpower():
    data = cr.get_total_consumption()

    return jsonify({'totalpower': data})


@app.route('/energy/consumption', methods=['GET'])
@TM.token_required
@trust_manager.discrete
def energy_consumption():
    consumption = cr.get_iot_consumption()
    json = []
    for i in range(len(consumption)):
        json.append({"resource": consumption[i][0], "values": consumption[i][1]})
    return jsonify(json)


@app.route('/energy/generation', methods=['GET'])
@TM.token_required
@trust_manager.discrete
def energy_generation():
    generation = cr.get_iot_generation()
    json = []
    for i in range(len(generation)):
        json.append({"resource": generation[i][0], "values": generation[i][1]})
    return jsonify(json)


@app.route('/energy/flexibility', methods=['GET'])
@TM.token_required
@trust_manager.discrete
def energy_flexibility():
    flexibility = cr.get_total_consumption() * random.randrange(0, 20) / 100
    return jsonify({'flexibility': flexibility})

@app.route('/shifting', methods=['GET'])
@TM.token_required
@trust_manager.community_manager
def get_shifting():
    iots = cr.get_forecasted_flexibility()
    building_service = BuildingService()
    [shift_kwh, shift_hours] = building_service.get_shift_hours_kwh(iots)
    return jsonify({'shift_hours': shift_hours, 'shift_kwh': shift_kwh})


@app.route('/invitation/get', methods=['POST'])
@TM.token_required
@trust_manager.community_manager
def get_invitation():
    json = request.get_json()
    event_time = json['event_time']

    dr_service = DemandResponseService()
    datetime, event_time, load_kwh, load_percentage, response = dr_service.get_invitation(event_time)
    return jsonify(
        {'datetime': datetime, "event_time": event_time, "load_kwh": load_kwh, "load_percentage": load_percentage,
         "response": response})


@app.route('/invitation/unanswered', methods=['GET'])
@TM.token_required
@trust_manager.community_manager
def get_unanswered_invitations():
    dr_service = DemandResponseService()
    invitations = dr_service.get_unanswered_invitations()
    return jsonify({'invitations': invitations})


@app.route('/invitation/answered', methods=['GET'])
@TM.token_required
@trust_manager.community_manager
def get_answered_invitations():
    dr_service = DemandResponseService()
    invitations = dr_service.get_answered_invitations()
    return jsonify({'invitations': invitations})


@app.route('/invitation/answer', methods=['POST'])
@TM.token_required
@trust_manager.community_manager
def answer_invitation():
    json = request.get_json()
    event_time = json['event_time']
    response = json['response']
    dr_service = DemandResponseService()
    dr_service.answer_invitation(event_time, response)
    return jsonify({'response': response})


@app.route('/invitation/send', methods=['POST'])
@TM.token_required
@trust_manager.community_manager
def invitation():
    json = request.get_json()
    event_time = json['event_time']
    load_kwh = json['kwh']
    load_percentage = json['percentage']
    iots = json['iots']
    print(event_time, load_kwh, load_percentage, iots)
    dr_service = DemandResponseService()
    dr_service.invitation(event_time, load_kwh, load_percentage, iots)
    return jsonify({'event_time': event_time})


@app.route('/invitation/auto', methods=['GET'])
@TM.token_required
def get_auto_answer():
    dr_service = DemandResponseService()
    auto_answer = dr_service.get_auto_answer_config()
    return jsonify({'auto_answer': auto_answer})


@app.route('/invitation/auto', methods=['POST'])
@TM.token_required
def auto_answer():
    json = request.get_json()
    auto_answer = json['auto_answer']
    dr_service = DemandResponseService()
    dr_service.set_auto_answer_config(auto_answer)
    return jsonify({'response': "OK"})


@app.route('/benefit', methods=['POST'])
@TM.token_required
def benefit():
    json = request.get_json()
    iot = json['iot']
    value = json['value']
    dr_service = DemandResponseService()
    dr_service.add_benefit(iot, value)
    return jsonify({'response': "OK"})


@app.route('/benefit/historic', methods=['GET'])
@TM.token_required
def get_benefit():
    dr_service = DemandResponseService()
    dr_service.get_benefit_historic()
    return jsonify({'response': "OK"})

if __name__ == "__main__":
    cr = Core()
    # cr.daemon = True
    cr.start()

    config = utils.get_config()
    app.run(host='0.0.0.0', port=config['app']['port'])
    cr.join()
