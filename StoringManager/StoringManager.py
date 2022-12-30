import sys
from threading import Thread

from Building.BuildingRepository import BuildingRepository

sys.path.append(".")
from time import time, sleep
from datetime import datetime
class StoringManager(Thread):
    def __init__(self, core):
        Thread.__init__(self)
        self.core = core

    #Erase consumption from the database
    def erase_consumption(self):
        
        return

    #Stop Monitoring
    def stop_saving(self):
        sys.exit()
        return
    
    #save consumption to a database
    def save_consumption(self):
        building_repo = BuildingRepository()
        #inserir objeto em forma de dicionario em mongodb
        for i in self.core.iots:
            building_repo.insert_iot(i.name, i.type, i.values, str(datetime.now()))
    
    def save_total_consumption(self):
        building_repo = BuildingRepository()
        building_repo.insert_totalpower(self.core.getTotalConsumption(), str(datetime.now()))
        

    #run method of thread monitoring 
    #get consumption per x time
    #second by second
    #ver consumos da sala x
    #calcular de hora em hora
    def run(self):
        while True:
            #sleep(self.core.config["storage"]["storing_frequency"] - time() % 1)
            sleep(5 - time() % 1)
            self.save_consumption() #save é o antigo saveConsumption
            self.save_total_consumption()
            #OU
            #for iot in core.iots:
                #save(iot)
        return



       