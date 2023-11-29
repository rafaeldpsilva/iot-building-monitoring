from database.DivisionRepository import DivisionRepository
from database.BuildingRepository import BuildingRepository
import pandas as pd
from datetime import datetime, timedelta
from modules import ACStatusAdapter
class DivisionService:
    def __init__(self):
        self.divisions_repo = DivisionRepository()

    def set_ac_status_model_configuration(self, historic_interval, outside_temperature_iot, outside_temperature_tag,
                                          temperature_iot, temperature_tag, humidity_iot, humidity_tag, light_iot,
                                          light_tag, division):
        considered_iots = [outside_temperature_iot, temperature_iot, humidity_iot, light_iot]
        outside_temperature_colname = outside_temperature_iot + '_' + outside_temperature_tag
        temperature_colname = temperature_iot + '_' + temperature_tag
        humidity_colname = humidity_iot + '_' + humidity_tag
        light_colname = light_iot + '_' + light_tag

        self.divisions_repo.set_ac_status_model_configuration(historic_interval, considered_iots,
                                                              outside_temperature_colname, temperature_colname,
                                                              humidity_colname, light_colname,division)

    def get_ac_status(self):
        building_repo = BuildingRepository()
        df = pd.DataFrame(building_repo.get_historic(datetime.now() - timedelta(hours=1)))
        df = df.drop("_id", axis=1)

        config = self.divisions_repo.get_ac_status_configuration()
        aux = pd.DataFrame()
        for i, row in df.iterrows():
            new = pd.DataFrame()
            for iot in row['iots']:
                if iot['name'] in config['considered_iots']:
                    for value in iot['values']:
                        val = value['values']
                        new[iot['name'] + '_' + value['type']] = [val]

            aux = pd.concat([aux, new])

        aux.rename(columns={'Temperature Sensor 103_temperature': 'Temperature (Cº)',
                            'Humidity Sensor 103_humidity': 'Humidity (%)', 'Light Sensor 103_light': 'Light (%)'},
                   inplace=True)

        aux['Temperature (Cº)'] = aux['Temperature (Cº)'] / 10
        aux['Humidity (%)'] = aux['Humidity (%)'] / 10
        aux['Light (%)'] = aux['Light (%)'] / 10
        aux['Heat Index (ºC)'] = ACStatusAdapter.calculate_heat_index_custom_celsius(aux['Temperature (Cº)'], aux['Humidity (%)'])
        aux['Outside temperature (ºC)'] = aux['Temperature (Cº)'] - 4

        #Talvez calcular media
        return ACStatusAdapter.predict_ac_status(aux.tail(1)['Outside temperature (ºC)'], aux.tail(1)['Temperature (Cº)'], aux.tail(1)['Heat Index (ºC)'], aux.tail(1)['Light (%)'])


    def get_divisions(self):
        divisions = self.divisions_repo.get_divisions()
        div = []
        for division in divisions:
            div.append({'name': division['name'], "iots": division['iots']})
        return div

    def insert_division(self, name, iots):
        # verify if iots exist
        # verify if name is not duplicate
        return self.divisions_repo.insert_division(name, iots)

