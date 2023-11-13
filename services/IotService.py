from datetime import datetime, timedelta
import random

import pandas as pd

from database.IotRepository import IotRepository
from modules.ForecastAdapter import ForecastAdapter
from modules import BatteryCommunicationAdapter


class IotService:
    def __init__(self):
        self.iot_repo = IotRepository()

    def get_iots(self):
        return self.iot_repo.get_iots()