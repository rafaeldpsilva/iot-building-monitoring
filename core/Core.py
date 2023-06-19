import random
import sys
import threading
from threading import Thread

sys.path.append(".")
from utils.utils import get_config
from model.IoT import IoT
from model.StoringManager import StoringManager
from model.Monitoring import Monitoring

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []

    def run_thread_schedule(self, job):
        forecast = threading.Thread(target=job)
        forecast.start()
        return

    def run(self):
        config = get_config()

        for i in config["resources"]["iots"]:
            iot = IoT(i, config['resources']['monitoring_period'])
            iot.daemon = True
            iot.start()
            self.iots.append(iot)

        storing_manager = StoringManager(self, config['storage']['storing_frequency'], config['app']['hour_offset'])
        storing_manager.daemon = True
        storing_manager.start()

        if not config['app']['monitoring']:
            monitoring = Monitoring(self)
            monitoring.daemon = True
            monitoring.start()

        #for i, iot in enumerate(self.iots):
        #    iot.join()

        #storing_manager.join()
        #if not config['app']['monitoring']:
        #    monitoring.join()

    def get_total_consumption(self):
        totalPower = 0
        for iot in self.iots:
            totalPower += iot.get_power()
        return totalPower
    
    def get_total_generation(self):
        total_generation = 0
        for iot in self.iots:
            if iot.type == "generation":
                total_generation += iot.get_generation()
        return total_generation

    def get_total_current(self):
        totalCurrent = 0
        for iot in self.iots:
            totalCurrent += iot.get_current()
        return totalCurrent

    def get_iot_consumption(self):
        iot_consumption = []
        for iot in self.iots:
            if iot.type != "generation":
                iot_consumption.append([iot.name, iot.get_power()])
        return iot_consumption

    def get_iot_generation(self):
        iot_generation = []
        for iot in self.iots:
            if iot.type == "generation":
                iot_generation.append([iot.name, iot.get_generation()])
        return iot_generation

    def get_forecasted_flexibility(self):
        forecasted_flexibility = []
        for iot in self.iots:
            forecasted_flexibility.append([iot.name, iot.get_power() * random.randrange(0,20)/100])
        return forecasted_flexibility
