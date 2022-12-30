import sys
from datetime import datetime
from threading import Thread
from time import time, sleep

sys.path.append(".")


class Monitoring(Thread):
    def __init__ (self, core):
        Thread.__init__(self)
        self.core = core

    #Stop Monitoring
    def stop_monitoring(self):
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



       