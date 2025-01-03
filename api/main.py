import random
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.append('.')
from services.IotService import IotService
from services.DivisionService import DivisionService
from services.P2PService import P2PService
from services.BatteryService import BatteryService
from services.BuildingService import BuildingService
from services.ForecastService import ForecastService
from services.TokenService import TokenService
from services.EnergyService import EnergyService
from services.DemandResponseService import DemandResponseService
from core.Core import Core
from utils import utils

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


@app.route('/', methods=['GET'])
def home():
    return jsonify({'online': True})


@app.route('/tokens', methods=['GET'])
def get_token_list():
    token_service = TokenService()
    tokens = token_service.get_tokens()
    return jsonify({'tokens': tokens})


@app.route('/tokens/generate', methods=['GET', 'POST'])
def generate_token():
    token = ''
    json = request.get_json()
    if request.method == 'POST':
        token_service = TokenService()
        token = token_service.generate_token(app.config['SECRET_KEY'], json.get("name"), json.get("list_of_resources"),
                                             json.get("data_aggregation"), json.get("time_aggregation"),
                                             json.get("embargo"), json.get("exp"))
    return jsonify({'token': token})


@app.route('/tokens/check', methods=['POST'])
def check_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.decode_token(token)

    return jsonify(token)


@app.route('/tokens/save', methods=['POST'])
def save_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.insert_token(token)

    return jsonify({'token': token['token'], 'datetime': token['datetime'], 'active': token['active']})


@app.route('/tokens/revoke', methods=['POST'])
def revoke_token():
    token = request.get_json().get("token")

    token_service = TokenService()

    token = token_service.revoke_token(token)

    return jsonify({'token': token['token'], 'datetime': token['datetime'], 'active': token['active']})


@app.route('/overview', methods=['GET'])
def overview():
    building_service = BuildingService()
    historic_overview = building_service.get_historic_overview()
    forecast_service = ForecastService()
    forecast = forecast_service.forecast_consumption()
    return jsonify({'historic': historic_overview, 'forecast': forecast})

@app.route('/historic', methods=['GET'])
def historic():
    building_service = BuildingService()
    historic_last_day = building_service.get_historic_last_day_by_hour()
    return jsonify({'historic': historic_last_day})

#!TODO USE TOTALPOWER ON THIS INSTEAD OF IOTREADINGS
@app.route('/historic/interval', methods=['POST'])
def energy_consumption_interval():
    json = request.get_json()
    start = json['start']
    building_service = BuildingService()
    consumption, generation, instants = building_service.get_mean_values(start)
    return jsonify({'consumption': consumption, 'generation': generation, "instants": instants})


@app.route('/iots', methods=['GET'])
def get_iots():
    iot_service = IotService()
    iots = iot_service.get_iots()
    return jsonify({'iots': iots})


@app.route('/batteries', methods=['GET'])
def get_batteries():
    batteries_service = BatteryService()
    batteries = batteries_service.get_batteries()
    return jsonify({'batteries': batteries})


@app.route('/batteries/historic', methods=['GET'])
def get_last_day_batteries():
    batteries_service = BatteryService()
    historic_last_day = batteries_service.get_batteries_historic_last_day()
    return jsonify({'historic': historic_last_day})


@app.route('/batteries/charge', methods=['POST'])
def charge_battery():
    json = request.get_json()
    battery = json['battery']
    quantity = json['quantity']
    batteries_service = BatteryService()
    batteries_service.charge_battery(battery, quantity)
    return jsonify({'response': True})


@app.route('/energy/now', methods=['GET'])
def energy_now():
    consumption = cr.get_total_consumption()
    generation = cr.get_total_generation()

    return jsonify({'consumption': consumption, 'generation': generation,
                    'flexibility': consumption * random.randrange(0, 20) / 100})


@app.route('/energy/totalpower', methods=['GET'])
def energy_totalpower():
    data = cr.get_total_consumption()

    return jsonify({'totalpower': data})


@app.route('/energy/consumption', methods=['GET'])
def energy_consumption():
    consumption = cr.get_iot_consumption()
    json = []
    for i in range(len(consumption)):
        json.append({"resource": consumption[i][0], "values": consumption[i][1]})
    return jsonify(json)


@app.route('/energy/generation', methods=['GET'])
def energy_generation():
    generation = cr.get_iot_generation()
    json = []
    for i in range(len(generation)):
        json.append({"resource": generation[i][0], "values": generation[i][1]})
    return jsonify(json)


@app.route('/energy/flexibility', methods=['GET'])
def energy_flexibility():
    flexibility = cr.get_total_consumption() * random.randrange(0, 20) / 100
    return jsonify({'flexibility': flexibility})


@app.route('/forecast/consumption', methods=['GET'])
def forecast_consumption():
    forecast_service = ForecastService()
    forecasted_consumption = forecast_service.forecast_consumption()

    return jsonify({'forecasted_consumption': forecasted_consumption})

@app.route('/forecast/generation', methods=['GET'])
def forecast_generation():
    forecast_service = ForecastService()
    forecasted_generation = forecast_service.forecast_generation()

    return jsonify({'forecasted_generation': forecasted_generation})

@app.route('/forecast/flexibility', methods=['GET'])
def forecast_flexibility():
    forecast_service = ForecastService()
    forecasted_flexibility = forecast_service.forecast_flexibility()
    return jsonify({'forecasted_flexibility': forecasted_flexibility}) 

@app.route('/iots/forecast/flexibility', methods=['POST'])
def iots_forecast_flexibility():
    json = request.get_json()
    hour = json['hour']
    shifting, reducing = cr.get_forecasted_flexibility(hour)
    return jsonify({'shifting': shifting, 'reducing': reducing})


@app.route('/iots/forecast/consumption', methods=['POST'])
def iots_forecast_consumption():
    json = request.get_json()
    hour = json['hour']
    consumption = cr.get_forecasted_consumption(hour)
    return jsonify({'forecasted_consumption': consumption})

@app.route('/forecast', methods=['GET'])
def forecast_value():
    forecast_service = ForecastService()
    df = forecast_service.forecast_value()

    return app.response_class(
        response=df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

@app.route('/invitation/get', methods=['POST'])
def get_invitation():
    json = request.get_json()
    event_time = json['event_time']

    dr_service = DemandResponseService()
    datetime, event_time, load_kwh, load_percentage, response = dr_service.get_invitation(event_time)
    return jsonify(
        {'datetime': datetime, "event_time": event_time, "load_kwh": load_kwh, "load_percentage": load_percentage,
         "response": response})


@app.route('/invitation/unanswered', methods=['GET'])
def get_unanswered_invitations():
    dr_service = DemandResponseService()
    invitations = dr_service.get_unanswered_invitations()
    return jsonify({'invitations': invitations})


@app.route('/invitation/answered', methods=['GET'])
def get_answered_invitations():
    dr_service = DemandResponseService()
    invitations = dr_service.get_answered_invitations()
    return jsonify({'invitations': invitations})


@app.route('/invitation/answer', methods=['POST'])
def answer_invitation():
    json = request.get_json()
    event_time = json['event_time']
    response = json['response']
    dr_service = DemandResponseService()
    dr_service.answer_invitation(event_time, response)
    return jsonify({'response': response})


@app.route('/invitation/send', methods=['POST'])
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
def get_auto_answer():
    dr_service = DemandResponseService()
    auto_answer = dr_service.get_auto_answer_config()
    return jsonify({'auto_answer': auto_answer})


@app.route('/invitation/auto', methods=['POST'])
def auto_answer():
    json = request.get_json()
    auto_answer = json['auto_answer']
    dr_service = DemandResponseService()
    dr_service.set_auto_answer_config(auto_answer)
    return jsonify({'response': "OK"})


@app.route('/event/check', methods=['POST'])
def event_check():
    json = request.get_json()
    event_time = json['event_time']
    iot_name = json['iot']
    cr.schedule_event(event_time, iot_name)
    return jsonify(True)

@app.route('/audit/check', methods=['GET'])
def audit_check():
    return jsonify({'response': "OK"})


@app.route('/dr/benefit', methods=['POST'])
def dr_benefit():
    json = request.get_json()
    iot = json['iot']
    value = json['value']
    service = EnergyService()
    service.add_benefit('dr',iot, value)
    return jsonify({'response': "OK"})

@app.route('/p2p/benefit', methods=['POST'])
def p2p_benefit():
    json = request.get_json()
    peer = json['peer']
    value = json['value']
    dr_service = EnergyService()
    dr_service.add_benefit('p2p',peer, value)
    return jsonify({'response': "OK"})

@app.route('/benefit/historic', methods=['GET'])
def get_benefit():
    dr_service = DemandResponseService()
    dr_service.get_benefit_historic()
    return jsonify({'response': "OK"})

@app.route('/iot/values', methods=['POST'])
def get_iot_values():
    json = request.get_json()
    iot = json['iot']
    values = cr.get_iot_values(iot)
    return jsonify(values)
    
@app.route('/iot/historic', methods=['POST'])
def get_iot_historic():
    json = request.get_json()
    iot = json['iot']
    iot_service = IotService()
    historic = iot_service.get_iot_historic(iot)
    return jsonify({'historic': historic})

@app.route('/iot/demandresponse/enable', methods=['POST'])
def change_dr_enable():
    json = request.get_json()
    iot = json['iot']
    enable = json['enable']
    iot_service = IotService()
    iot_service.change_dr_enable(iot, enable)
    return jsonify(True)

@app.route('/iot/instructions', methods=['POST'])
def instructions():
    json = request.get_json()
    instructions = json['instructions']
    iot_service = IotService()
    iot_service.update_instructions(instructions)
    cr.set_instructions(instructions)
    return jsonify(True)

@app.route('/iot/instructions', methods=['GET'])
def get_instructions():
    iot_service = IotService()
    instructions = iot_service.get_instructions()
    return jsonify(instructions)

@app.route('/divisions', methods=['GET'])
def get_divisions():
    division_service = DivisionService()
    divisions = division_service.get_divisions()
    return jsonify({"divisions": divisions})


@app.route('/divisions/create', methods=['POST'])
def create_division():
    json = request.get_json()
    name = json['name']
    iots = json['iots']
    division_service = DivisionService()
    division_service.insert_division(name, iots)
    return jsonify(True)


@app.route('/divisions/update', methods=['POST'])
def update_division():
    json = request.get_json()
    division_service = DivisionService()
    division_service.update_division(json['id'], json['name'], json['iots'], json['ac_status_configuration'])
    return jsonify(True)


@app.route('/divisions/acstatus', methods=['POST'])
def get_ac_status():
    json = request.get_json()
    division_service = DivisionService()
    ac_status = division_service.get_ac_status(json['id'])
    if ac_status == 1:
        ac_status = "on-cold"
    elif ac_status == -1:
        ac_status = "on-warm"
    else:
        ac_status = "off"

    return jsonify({"ac_status": ac_status})


@app.route('/p2p/prices', methods=['POST'])
def post_prices():
    json = request.get_json()
    sell_percentage = json['sell_percentage']
    buy_percentage = json['buy_percentage']
    p2p_service = P2PService()
    p2p_service.update_prices(sell_percentage, buy_percentage)
    return jsonify(True)


@app.route('/p2p/prices', methods=['GET'])
def get_prices():
    p2p_service = P2PService()
    prices = p2p_service.get_prices()
    return jsonify({"prices": prices})

@app.route('/p2p/transaction', methods=['POST'])
def set_bids():
    json = request.get_json()
    hour = json['hour']
    peer = json['peer']
    quantity = json['quantity']
    cost = json['cost']
    p2p_service = P2PService()
    p2p_service.set_transaction(hour, peer, quantity, cost)
    return jsonify(True)

@app.route('/energy/selfconsumption', methods=['GET'])
def get_self_consumption():
    energy_service = EnergyService()
    self_consumption = energy_service.get_self_consumption()
    return jsonify({"self_consumption": self_consumption})

@app.route('/energy/retailer', methods=['GET'])
def get_retailer():
    energy_service = EnergyService()
    retailer = energy_service.get_energy_from_retailer()
    return jsonify({"retailer": retailer})

@app.route('/energy/co2/p2p', methods=['GET'])
def get_co2_with_p2p():
    energy_service = EnergyService()
    co2_with_p2p = energy_service.get_co2_with_p2p()
    return jsonify({"co2": co2_with_p2p})

@app.route('/energy/co2', methods=['GET'])
def get_co2_without_p2p():
    energy_service = EnergyService()
    co2_without_p2p = energy_service.get_co2_without_p2p()
    return jsonify({"co2": co2_without_p2p})

@app.route('/benefits/monthly', methods=['GET'])
def get_monthly_benefits():
    energy_service = EnergyService()
    monthly_benefits = energy_service.get_monthly_benefits()
    return jsonify(monthly_benefits)

@app.route('/benefits/detailed', methods=['GET'])
def get_benefits():
    energy_service = EnergyService()
    benefits = energy_service.get_benefits()
    return jsonify({'benefits':benefits})

if __name__ == "__main__":
    cr = Core()
    cr.start()

    config = utils.get_config()
    app.run(host='0.0.0.0', port=config['app']['port'])
    cr.join()
