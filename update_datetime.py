import pandas as pd
from datetime import datetime
from database.BuildingRepository import BuildingRepository

start = "2023-05-30 12:00:00"
building_repo = BuildingRepository()
total = building_repo.get_historic_update(start)