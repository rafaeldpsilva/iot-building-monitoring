from datetime import datetime, timedelta

import pandas as pd

from database.BatteryRepository import BatteryRepository
from modules import BatteryCommunicationAdapter


class BatteryService:
    def __init__(self):
        self.battery_repo = BatteryRepository()

    def get_batteries(self):
        batteries = self.battery_repo.get_batteries()
        if len(batteries) == 0:
            return []

        for battery in batteries:
            battery['charging_rate'] = BatteryCommunicationAdapter.get_battery_charging_rate(battery['ip'])
            battery['charge'] = BatteryCommunicationAdapter.get_battery_state_of_charge(battery['ip'])

        return batteries

    def get_batteries_historic_last_day(self):
        total = self.battery_repo.get_batteries_historic(
            datetime.strftime(datetime.now() - timedelta(hours=24), "%Y-%m-%d %H:%M:%S"))
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
        total = total.dropna()
        total = total.values.tolist()

        batteries_energy = []
        for row in total:
            batteries = row[0]
            date = row[1]
            stored_energy = 0

            cena = []
            for battery in batteries:
                for value in battery['values']:
                    if 'values' in value:
                        if value['tag'] == "battery.stored_energy":
                            stored_energy += value['values']
                            cena.append(round(value['values'], 2))
            aux = [date, round(stored_energy / len(batteries), 2)]
            aux.extend(cena)
            batteries_energy.append(aux)
        names = ['datetime', 'stored_energy']

        batteries = total[0][0]
        for battery in batteries:
            names.append(battery['name'])

        total = pd.DataFrame(batteries_energy, columns=names)
        total['datetime'] = pd.to_datetime(total['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        total.set_index("datetime", inplace=True)
        total = total.resample('1H').mean()
        total = total.tail(24)
        total['datetime'] = total.index
        total = total.values.tolist()
        return total

    def charge_battery(self, battery, quantity):
        batteries = self.battery_repo.get_batteries()
        for bat in batteries:
            if bat['name'] == battery:
                BatteryCommunicationAdapter.charge_battery(bat['ip'], quantity)
