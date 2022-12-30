from datetime import datetime
from threading import Thread
import threading
import sys
import json
from time import time, sleep
sys.path.append(".")
from IOTClass.IoT import IoT


class monitoring(Thread):
    def __init__ (self, core):
        Thread.__init__(self)
        self.core = core

    #Stop Monitoring
    def stopMonitoring(self):
        sys.exit()
        return

    def run(self):
        sleep(5 - time() % 1)
        while True:
            sleep(1 - time() % 1)
            print(datetime.now())
            print("Total consumption: " + str(self.core.getTotalConsumption()))
            print("Total current: " + str(self.core.getTotalCurrent()))
            print()
        return



       