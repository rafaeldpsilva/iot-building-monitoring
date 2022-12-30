from asyncio.windows_events import NULL
from flask import Flask, jsonify, request, make_response
import jwt 
import sys
sys.path.append('.')
import datetime
from functools import wraps
from pymongo import MongoClient
import json
import APIToken_Manager.tokenManager as TM
from bson import ObjectId
from flask_cors import CORS
from bson.json_util import dumps
import pandas as pd
import pymongo
from Core import core

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)

cr = core()
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


@app.route('/', methods=['GET', 'POST'])
def home():
    return 

@app.route('/building/energy', methods=['GET', 'POST'])
@TM.token_required
def protected():
    x = []
    
    if TM.dados['Data Aggregation'] == 'individual':
        for i in TM.dados['List of Resources']:
            for iot in cr.iots:
                if i['text'] == iot.name and i['text'] != 'Generation':
                    x.append({"resource": iot.name, "values": iot.getPower()})
                
                if i['text'] == iot.name and i['text'] == 'Generation':
                    x.append({"resource": iot.name, "values": iot.getGeneration()})
    else:
        x = {"resource": "end-user", "values": 0}
        for i in TM.dados['List of Resources']:
            for iot in cr.iots:
                if i['text'] == iot.name:
                    x['values'] += iot.getPower() 
    
    return jsonify({'consumption': x})

@app.route('/generate_token', methods=['GET', 'POST'])
def generate():
    token= ''

    if request.method == 'POST':
        token = jwt.encode({
            'Name' : request.get_json().get("name"), 
            'List of Resources' : request.get_json().get("listofresources"), 
            'Data Aggregation' : request.get_json().get("dataaggregation"), 
            'Time Aggregation' : request.get_json().get("timeaggregation"), 
            'Embargo Period' : request.get_json().get("embargo"),
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes = request.get_json().get("exp"))
        }, 
        app.config['SECRET_KEY'],
        algorithm = "HS256")
    
    #fetch data from the database
    with open('./config/config.json') as config_file:
        config = json.load(config_file)

    #conectar ao servidor e à base de dados
    client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
    
    db1 = client.Tokens_leftside
        
    #criar a tabela
    tokensdb = db1.tokencol

    #inserir objeto em forma de dicionario em mongodb
    tokensdb.insert_one({"token": token,
                "expiration_time_minutes" : request.get_json().get("exp"),
                "datetime": datetime.datetime.now(),
                "active": True})
                
    return jsonify({'token':token})

@app.route('/building/historic', methods=['GET', 'POST'])
@TM.token_required
def protectedhist():
    with open('./config/config.json') as config_file:
        data1 = json.load(config_file)

    #connecting to database
    client = MongoClient(str(data1['storage']['local']['server']) + ':' + str(data1['storage']['local']['port']))
    db = client.BuildingRightSide
    col = db.iots_reading
    x = []

    time = datetime.datetime.now() - datetime.timedelta(minutes=180) 
    timeemb = datetime.datetime.now() - datetime.timedelta(minutes=int(TM.dados['Embargo Period']))
    
    indexArray = []
    dataArray = []
    columns = []
    if TM.dados['Data Aggregation'] == 'sum':
        columns.append("end-user")
    getIndex = True;
    for i in TM.dados['List of Resources']:
        x = col.find( {"name": i['text'], 'datetime': { '$gt': str(time), '$lt' : str(timeemb)} } )
        y = list(x)
        if TM.dados['Data Aggregation'] == 'individual':
            columns.append(i['text'])
        index = 0
        for entry in y:
            if getIndex:
                indexArray.append(datetime.datetime.strptime(entry["datetime"][:19], "%Y-%m-%d %H:%M:%S"))
                dataArray.append([])
                if TM.dados['Data Aggregation'] == 'sum':
                    dataArray[index].append(0)
            if TM.dados['Data Aggregation'] == 'individual':
                dataArray[index].append(getvalue(entry['iot_values'], 'power'))
            else:
                dataArray[index][0] += getvalue(entry['iot_values'], 'power')
            index += 1
        if getIndex:
            getIndex = False

    df = pd.DataFrame(dataArray, index=indexArray, columns=columns)

    if TM.dados["Time Aggregation"] == "5minutes":
        df=df.groupby(df.index.floor('5T')).mean()
    elif TM.dados["Time Aggregation"] == "15minutes":
        df=df.groupby(df.index.floor('15T')).mean()
    elif TM.dados["Time Aggregation"] == "60minutes":
        df=df.groupby(df.index.floor('60T')).mean()
    
    return app.response_class(
        response= df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

@app.route('/building/rightside/totalpower', methods=['GET', 'POST'])
@TM.token_required
def rightside():
    data = cr.getTotalConsumption()

    return jsonify({'totalpower': data})

@app.route('/building/rightside/generation', methods=['GET', 'POST'])
@TM.token_required
def rightsidegeneration():
    for iot in cr.iots:
        data = iot.getGeneration()

    return jsonify({'Generation' : data})

@app.route('/building/correlations', methods=['GET', 'POST'])
def correlations():
    return

@app.route('/building/forecast', methods=['GET'])
@TM.token_required
def forecast():
    with open('./config/config.json') as config_file:
        data1 = json.load(config_file)

    #connecting to database
    client = MongoClient(str(data1['storage']['local']['server']) + ':' + str(data1['storage']['local']['port']))
    db = client.ForecastDay
    col = db.forecastvalue
    x = col.find().sort("_id", pymongo.DESCENDING).limit(1)
    y = list(x)
    df = pd.DataFrame(y)
    
    df.drop('_id', inplace=True, axis=1)
    # df = df.iloc[1: , :]
    # print(df)
    # df.drop('0', inplace=True, axis=1)
    # df_n = df.set_index('datetime')
    # reversed_df = df_n.iloc[::-1]

    return app.response_class(
        response= df.to_json(orient='index', date_format='iso'),
        status=200,
        mimetype='application/json'
    )

def getvalue(array, type):
    for value in array:
        if value['type'] == type:
            #print(value)
            return (value['values'])
    return -1

if __name__ == "__main__":
    cr.setDaemon(True)
    cr.start()

    app.run(host='0.0.0.0', port=5002)
    cr.join()