import sys
from threading import Thread
from time import time, sleep
from datetime import datetime
sys.path.append(".")
from database.BuildingRepository import BuildingRepository

class StoringManager(Thread):
    def __init__(self, core, storing_frequency):
        Thread.__init__(self)
        self.core = core
        self.storing_frequency = storing_frequency

    #Erase consumption from the database
    def erase_consumption(self):
        return

    #Stop Monitoring
    def stop_saving(self):
        sys.exit()

    #save consumption to a database
    def save_consumption(self):
        building_repo = BuildingRepository()
        #inserir objeto em forma de dicionario em mongodb
        for i in self.core.iots:
            building_repo.insert_iot(i.name, i.type, i.values, str(datetime.now()))

    def save_total_consumption(self):
        building_repo = BuildingRepository()
        building_repo.insert_totalpower(self.core.get_total_consumption(), str(datetime.now()))

    def run(self):
        while True:
            #sleep(self.core.config["storage"]["storing_frequency"] - time() % 1)
            sleep(5 - time() % 1)
            self.save_consumption() #save é o antigo saveConsumption
            self.save_total_consumption()
            #OU
            #for iot in core.iots:
                #save(iot)
