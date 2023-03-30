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
        print(self.values) # [{type:, tag:, dataType:},{type:, tag:, dataType:}]
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
            if value["type"] == valueName:
                return value["values"]
        return 0
    
    def get_generation(self):
        for value in self.values:
            if value["type"] == "generation":
                return value["values"]
        return 0

    def update_values(self):
        response = None
        if (self.method == 'GET'):
            try:
                request = requests.get(self.uri)
                data_json = request.text
                response = json.loads(data_json)
            except requests.exceptions.HTTPError as error:
                print (error.response.text)
        else:
            try:
                request = requests.post(self.uri)
                data_json = request.text
                response = json.loads(data_json)
            except requests.exceptions.HTTPError as error:
                print (error.response.text)

        if response != None:
            try:
                for value in self.values:
                    tags = value['tag'].split('.')
                    path = response
                    
                    for tag in tags:
                        path = path[tag]
                    
                    if("multiplier" in value):
                        path *= value["multiplier"]
                    value['values'] = round(path, 4)
            except KeyError:
                print("\n\nKey Error in " + self.name)
            except TypeError:
                print("\n\nType Error in " + self.name)
        else:
            print("\n\n\n\n\nERROR! IN UPDATING VALUES OF IOT", self.name)

    def run(self):
        while True:
            sleep(self.monitoring_period - time() % 1)
            self.update_values()
