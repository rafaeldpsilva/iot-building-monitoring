from threading import Thread
from time import time, sleep

from utils import utils
import logging

class IoT(Thread):
    def __init__(self, config, config_monitoring):
        Thread.__init__(self)
        self.name = config["name"]
        self.type = config["type"]
        self.uri = config["uri"]
        self.values = config["values"]
        self.control = config["control"]
        self.monitoring_period = config_monitoring
        # print(self.name, self.values) # [{type:, tag:, dataType:},{type:, tag:, dataType:}]

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
            if value["type"] == "current":
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
        response = utils.update_values_get(self.name, self.uri)

        if response != None:
            try:
                for value in self.values:
                    value['values'] = round(response, 4)
            except KeyError:
                logging.warning("Key Error in " + self.name + " with response " + response)
            except TypeError:
                logging.warning("Type Error in " + self.name)
        else:
            logging.warning("ERROR! IN UPDATING VALUES OF IOT " + self.name)

    def run(self):
        while True:
            sleep(self.monitoring_period - time() % 1)
            self.update_values()
