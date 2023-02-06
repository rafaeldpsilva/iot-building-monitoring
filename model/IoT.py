from __future__ import print_function

import json
from threading import Thread
from time import time, sleep
import requests


class IoT(Thread):
    def __init__(self, config, config_monitoring):
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
        self.monitoring_period = config_monitoring
        #self.store = iot_config.store

        #for value in self.values:
        #    value["value"] = 0
    
    def get_power(self):
        for value in self.values:
            if value["type"] == "power":
                return value["values"]
        return 0
    
    def get_voltage(self):
        for value in self.values:
            if value["type"] == "voltage":
                return value["values"]
        return 0
    
    def get_current(self):
        for value in self.values:
            if value["type"]  == "current":
                return value["values"]
        return 0

    def get_value(self, valueName):
        for value in self.values:
            if value["type"]  == valueName:
                return value["values"]
        return 0
    
    def get_generation(self):
        for value in self.values:
            if value["type"] == "generation":
                return value["values"]
        return 0

    #methods to get data from iot devices
    def update_values(self):
        data = None
        while(data is None):
            if (self.method == 'GET'):
                try:
                    request = requests.get(self.uri) # tem de se validar o self.method porque pode ser post
                    data_json = request.text
                    data = json.loads(data_json)
                except requests.exceptions.HTTPError as error:
                    print (error.response.text)
            else:
                try:
                    request = requests.post(self.uri)
                    data_json = request.text
                    data = json.loads(data_json)
                except requests.exceptions.HTTPError as error:
                    print (error.response.text)


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
        while True:
            sleep(self.monitoring_period - time() % 1) # tempo dado no config (monitoring_period)
            self.update_values()

