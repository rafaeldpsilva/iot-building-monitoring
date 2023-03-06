import sys
import threading
from threading import Thread
import random
import time
import schedule

sys.path.append(".")
from utils.utils import get_config
from model.IoT import IoT
from model.StoringManager import StoringManager
from model.Monitoring import Monitoring

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []

    def get_forecasted_flexibility(self):
        forecasted_flexibility = []
        for iot in self.iots:
            forecasted_flexibility.append([iot.name, iot.get_power() * random.randrange(0,20)/100])
        return forecasted_flexibility

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

        storing_manager = StoringManager(self, config['storage']['storing_frequency'])
        storing_manager.daemon = True
        storing_manager.start()

        if not config['app']['monitoring']:
            monitoring = Monitoring(self)
            monitoring.daemon = True
            monitoring.start()

        #while 1:
        #    schedule.run_pending()
        #    time.sleep(1)

        for i in range(len(self.iots)):
            self.iots[i].join()

        storing_manager.join()
        monitoring.join()

    def get_total_consumption(self):
        totalPower = 0
        for iot in self.iots:
            totalPower += iot.get_power()
        return totalPower

    def get_total_current(self):
        totalCurrent = 0
        for iot in self.iots:
            totalCurrent += iot.get_current()
        return totalCurrent
