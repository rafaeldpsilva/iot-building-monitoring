from __future__ import print_function

import json
from threading import Thread
from time import time, sleep

import requests


class IoT(Thread):
    def __init__(self, config):
        Thread.__init__(self)
        self.name = config["name"]
        print(self.name)
        self.type = config["type"]
        self.uri = config["uri"]
        self.method = config["method"]
        self.body = config["body"]
        self.values = config["values"] 
        print(self.values) # [{type:, tag:, dataType:, value},{type:, tag:, dataType:, value}]
        self.control = config["control"]
        #self.store = iot_config.store

        #for value in self.values:
        #    value["value"] = 0
    
    def getPower(self):
        for value in self.values:
            if value["type"] == "power":
                return value["values"]
        return 0
    
    def getVoltage(self):
        for value in self.values:
            if value["type"] == "voltage":
                return value["values"]
        return 0
    
    def getCurrent(self):
        for value in self.values:
            if value["type"]  == "current":
                return value["values"]
        return 0

    def getValue(self, valueName):
        for value in self.values:
            if value["type"]  == valueName:
                return value["values"]
        return 0
    
    def getGeneration(self):
        for value in self.values:
            if value["type"] == "generation":
                return value["values"]
        return 0
    
    def getState(self):
        return self.state

    #methods to get data from iot devices
    def updateValues(self):
        data = None
        while(data is None):
            try:
                if (self.method == 'GET'):
                    request = requests.get(self.uri) # tem de se validar o self.method porque pode ser post
                    data_json = request.text
                    data = json.loads(data_json)
                else:
                    request = requests.post(self.uri)
                    data_json = request.text
                    data = json.loads(data_json)
            except:
                print('An exception ocurred')
        
        #ir buscar os valores dos analyzers
        for value in self.values:
            tags = value['tag'].split('.')
            path = data
            for tag in tags:
                path = path[tag]
            if("multiplier" in value):
                path *= value["multiplier"]
            value['values'] = round(path, 4)

    def run(self):
        #retirar daqui
        with open('./config/config.json') as config_file:
            data = json.load(config_file)

        while True:
            sleep(data['resources']['monitoring_period'] - time() % 1) # tempo dado no config (monitoring_period)
            self.updateValues()

