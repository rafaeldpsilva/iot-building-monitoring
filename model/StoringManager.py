import sys
from datetime import datetime
from threading import Thread
from time import time, sleep

sys.path.append(".")
from database.BuildingRepository import BuildingRepository

class StoringManager(Thread):
    def __init__(self, core, storing_frequency):
        Thread.__init__(self)
        self.core = core
        self.storing_frequency = storing_frequency

    def stop_saving(self):
        sys.exit()

    def save_iot_values(self):
        building_repo = BuildingRepository()
        iots = []
        for i in self.core.iots:
            iots.append({"name":i.name, "type":i.type, "values":i.values})
        building_repo.insert_iots(iots, str(datetime.now()))

    def save_total(self):
        building_repo = BuildingRepository()
        building_repo.insert_total(self.core.get_total_consumption(), self.core.get_total_generation(), str(datetime.now()))

    def run(self):
        while True:
            sleep(self.storing_frequency - time() % 1)
            self.save_iot_values()
            self.save_total()
