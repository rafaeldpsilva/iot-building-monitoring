from threading import Thread
import threading
import sys
import json
sys.path.append(".")
from pymongo import MongoClient
from IOTClass.IoT import IoT
from StoringManager.StoringManager import storing
import schedule
from Monitoring.Monitoring import monitoring
from Forecast.consumption_forecast import forecastday, forecasthour
import time

class core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []
    
    def run_thread_schedule(self, job):
        forecast = threading.Thread(target=job)
        forecast.start()
        return

    def run(self):
        #ler o ficheiro de configuração (decode do ficheiro)
        with open('./config/config.json') as config_file:
            config = json.load(config_file)

        #para cada elemento da key 'iots' dentro do ficheiro de configuração fazer
        for i in config["resources"]["iots"]:
            iot = IoT(i)
            iot.setDaemon(True)
            iot.start()
            self.iots.append(iot)
        
        #iniciar uma thread de storing (storing(self)) :: enviar o tempo de gravação da configuração (config[storage][storing_frequency])
        #start da thread de storing
        sto = storing(self)
        sto.setDaemon(True)
        sto.start()
        
        #iniciar uma thread de monitoring (monitoring(self))
        #start da thread de monitoring
        mon = monitoring(self)
        mon.setDaemon(True)
        mon.start()

        schedule.every().day.at("22:00").do(self.run_thread_schedule, forecastday)    
        
        while 1:
            schedule.run_pending()
            time.sleep(1)

        ########### o que isto faz é de segundo a segundo print(core.getTotalConsumption())
        #join das threads
        for i in range(len(self.iots)):
            self.iots[i].join()
        
        sto.join()
        mon.join()
        #iniciar os agendamentos dos forecasts (para cada um deles deve-se enviar o 'self')
        #schedule.every().day.at("22:00").do(forecastday())
        #schedule.every().hour.at(":15").do(forecasthour()) 
        
    def getTotalConsumption(self):
        totalPower = 0
        for iot in self.iots:
            totalPower += iot.getPower()
        return totalPower
        
    def getTotalCurrent(self):
        totalCurrent = 0
        for iot in self.iots:
            totalCurrent += iot.getCurrent()
        return totalCurrent


print("\nExiting the Program!!!")

