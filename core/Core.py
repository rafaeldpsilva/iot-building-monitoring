import random
import sys
import threading
from threading import Thread

sys.path.append(".")
from utils.utils import get_config
from model.IoT import IoT
from model.Battery import Battery
from model.StoringManager import StoringManager
from model.Monitoring import Monitoring
from core.DemandResponseAtuator import DemandResponseAtuator

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []
        self.iots_consumption = []
        self.iots_generation = []
        self.batteries = []
        self.dr_reduced_power = 0

    def run_thread_schedule(self, job):
        forecast = threading.Thread(target=job)
        forecast.start()
        return

    def run(self):
        config = get_config()

        for i in config["resources"]["iots"]:
            iot = IoT(i, config['resources']['monitoring_period'])
            # iot.daemon = True
            if i["store"]["type"] == "consumption":
                self.iots_consumption.append(iot)
            if i["store"]["type"] == "generation":
                self.iots_generation.append(iot)
            iot.start()
            self.iots.append(iot)

        for i in config["resources"]["batteries"]:
            battery = Battery(i, config['storage']['storing_frequency'])
            # battery.daemon = True
            battery.start()
            self.batteries.append(battery)

        storing_manager = StoringManager(self, config['storage']['storing_frequency'], config['app']['hour_offset'])
        # storing_manager.daemon = True
        storing_manager.start()

        if not config['app']['monitoring']:
            monitoring = Monitoring(self)
            # monitoring.daemon = True
            monitoring.start()

        # for i, iot in enumerate(self.iots):
        #    iot.join()

        # storing_manager.join()
        # if not config['app']['monitoring']:
        #    monitoring.join()

    def get_total_batteries_state(self):
        total_state = 0
        for bat in self.batteries:
            total_state += bat.get_charge_state()
        return total_state / len(self.batteries)

    def get_total_consumption(self):
        totalPower = 0
        for iot in self.iots_consumption:
            totalPower += iot.get_power()
        reduce = self.dr_reduced_power
        self.dr_reduced_power = 0
        return totalPower - reduce

    def get_total_generation(self):
        total_generation = 0
        for iot in self.iots_generation:
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
    
    def get_iot_values(self, name):
        for iot in self.iots:
            if iot.name == name:
                print(iot.values)
                return iot.values
        return False

    def get_forecasted_flexibility(self):
        shifting = []
        reducing = []
        for iot in self.iots:
            if iot.demandresponse == "shifting":
                shifting.append([iot.name, iot.get_power() * random.randrange(0, 20) / 100])
            if iot.demandresponse == "reducing":
                reducing.append([iot.name, iot.get_power() * random.randrange(0, 20) / 100])
        return shifting, reducing

    def get_forecasted_consumption(self):
        forecasted_consumption = []
        for iot in self.iots:
            if iot.demandresponse == 'shifting' or iot.demandresponse == 'reducing':
                forecasted_consumption.append([iot.name, iot.get_power()])
        return forecasted_consumption

    def schedule_event(self, event_time, iot_name):
        iot = None
        for i in self.iots:
            if i.name == iot_name:
                iot = i
        if iot is None:
            return False
        dr = DemandResponseAtuator(self, iot)
        dr.start()
