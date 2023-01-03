import sys
import threading
from threading import Thread
import time
import schedule
from IOTClass.IoT import IoT
from StoringManager.StoringManager import StoringManager
from Monitoring.Monitoring import Monitoring
from Forecast.consumption_forecast import forecastday
from Utils import utils

sys.path.append(".")

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.iots = []

    def run_thread_schedule(self, job):
        forecast = threading.Thread(target=job)  #!bad variable name
        forecast.start()
        return

    def run(self):
        #ler o ficheiro de configuração (decode do ficheiro)
        config = utils.get_config()

        #para cada elemento da key 'iots' dentro do ficheiro de configuração fazer
        for i in config["resources"]["iots"]:
            iot = IoT(i)
            iot.daemon = True
            iot.start()
            self.iots.append(iot)

        #iniciar uma thread de storing (storing(self)) :: enviar o tempo de gravação
        #da configuração (config[storage][storing_frequency])
        #start da thread de storing
        storing_manager = StoringManager(self)
        storing_manager.daemon = True
        storing_manager.start()

        #iniciar uma thread de monitoring (monitoring(self))
        #start da thread de monitoring
        monitoring = Monitoring(self)
        monitoring.daemon = True
        monitoring.start()

        schedule.every().day.at("22:00").do(self.run_thread_schedule, forecastday)    

        while 1:
            schedule.run_pending()
            time.sleep(1)

        ########### o que isto faz é de segundo a segundo print(core.get_total_consumption())
        #join das threads
        #!for i, iot in enumerate(self.iots):
        #!    v.join() 
        for i in range(len(self.iots)):
            self.iots[i].join()

        storing_manager.join()
        monitoring.join()
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
