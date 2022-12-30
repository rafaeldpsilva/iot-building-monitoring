from threading import Thread
import threading
import sys
import json
from pymongo import MongoClient
sys.path.append(".")
from time import time, sleep
from datetime import datetime


class storing(Thread):
    def __init__ (self, core):
        Thread.__init__(self)
        self.core = core

    #Erase consumption from the database
    def eraseConsumption(self):
        
        return

    #Stop Monitoring
    def stopSaving(self):
        sys.exit()
        return
    
    #save consumption to a database
    def save(self):

        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        #conectar ao servidor e à base de dados
        client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        
        db = client.BuildingRightSide
        
        #criar a tabela
        iots = db.iots_reading
        
        #inserir objeto em forma de dicionario em mongodb
        for i in self.core.iots:
            iots.insert_one({"name": i.name, 
                    "type": i.type, 
                    "iot_values" : i.values, 
                    "datetime" : str(datetime.now())})
    
    def savetotal(self):
        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        #conectar ao servidor e à base de dados
        client = MongoClient(str(config['storage']['local']['server']) + ':' + str(config['storage']['local']['port']))
        
        db = client.TotalPower
        
        #criar a tabela
        total = db.powerrightside
        
        #inserir objeto em forma de dicionario em mongodb
        total.insert_one({"totalpower": self.core.getTotalConsumption(), 
                    "datetime" : str(datetime.now())})

    #run method of thread monitoring
    #get consumption per x time
    #second by second
    #ver consumos da sala x
    #calcular de hora em hora
    def run(self):
        while True:
            #sleep(self.core.config["storage"]["storing_frequency"] - time() % 1)
            sleep(5 - time() % 1)
            self.save() #save é o antigo saveConsumption
            self.savetotal()
            #OU
            #for iot in core.iots:
                #save(iot)
        return



       