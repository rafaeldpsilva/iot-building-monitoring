import pandas as pd
import random
from database.BuildingRepository import BuildingRepository
from modules.ForecastAdapter import ForecastAdapter

def forecast_flexibility():
    building_repo = BuildingRepository()
    consumption = pd.DataFrame(building_repo.get_totalpower_col())
    consumption = consumption.drop("_id", axis=1)
    forecast_adapter = ForecastAdapter()
    return forecast_adapter.forecast_day_consumption(consumption)

#building_service = BuildingService()
#df = building_service.forecast_consumption()
array = forecast_flexibility().numpy().tolist()

flex = []
for val in array:
    flex.append(val * random.randrange(0,20)/100)

print(flex)