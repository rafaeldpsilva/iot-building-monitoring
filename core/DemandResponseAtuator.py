import time
from datetime import datetime
from threading import Thread
import schedule


class DemandResponseAtuator(Thread):
    def __init__(self, core, iot):
        Thread.__init__(self)
        self.iot = iot
        self.core = core
        self.event_on = True

    def end_event(self):
        self.event_on = False
        return schedule.CancelJob

    def run(self):
        now = datetime.now()
        end_time = now.replace(minute=59, second=0, microsecond=0)
        schedule.every().day.at(datetime.strftime(end_time, "%H:%M")).do(self.end_event)
        while self.event_on:
            self.core.dr_reduced_power += self.iot.get_power()
            schedule.run_pending()
            time.sleep(1)
