import sys
import threading
from threading import Thread
import time
import schedule
sys.path.append(".")
from utils.utils import get_config
from model.IoT import IoT
from model.StoringManager import StoringManager
from model.Monitoring import Monitoring
#from model.consumption_forecast import forecastday


class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []

    def run_thread_schedule(self, job):
        forecast = threading.Thread(target=job)
        forecast.start()
        return

    def run(self):
        #ler o ficheiro de configuração (decode do ficheiro)
        config = get_config()

        #para cada elemento da key 'iots' dentro do ficheiro de configuração fazer
        for i in config["resources"]["iots"]:
            iot = IoT(i, config['resources']['monitoring_period'])
            iot.daemon = True
            iot.start()
            self.iots.append(iot)

        #iniciar uma thread de storing (storing(self)) :: enviar o tempo de gravação
        #da configuração (config[storage][storing_frequency])
        #start da thread de storing
        storing_manager = StoringManager(self, config['resources']['monitoring_period'])
        storing_manager.daemon = True
        storing_manager.start()

        #iniciar uma thread de monitoring (monitoring(self))
        #start da thread de monitoring
        if config['app']['monitoring']:
            monitoring = Monitoring(self)
            monitoring.daemon = True
            monitoring.start()

        #schedule.every().day.at("22:00").do(self.run_thread_schedule, forecastday)    

        #while 1:
        #    schedule.run_pending()
        #    time.sleep(1)

        ########### o que isto faz é de segundo a segundo print(core.get_total_consumption())
        #join das threads
        #!for i, iot in enumerate(self.iots):
        #!    v.join() 
        for i in range(len(self.iots)):
            self.iots[i].join()

        storing_manager.join()
        #monitoring.join()
        #iniciar os agendamentos dos forecasts (para cada um deles deve-se enviar o 'self')
        #schedule.every().day.at("22:00").do(forecastday())
        #schedule.every().hour.at(":15").do(forecasthour()) 

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


print("\nExiting the Program!!!")
