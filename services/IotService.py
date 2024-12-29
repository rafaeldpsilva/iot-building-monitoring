from datetime import datetime, timedelta

import pandas as pd

from database.IotRepository import IotRepository


class IotService:
    def __init__(self):
        self.iot_repo = IotRepository()

    def get_iots(self):
        return self.iot_repo.get_iots()

    def get_iot_historic(self, iot_x: str):
        total = self.iot_repo.get_historic_by_interval(
            datetime.now() - timedelta(hours=24), datetime.now())
        total = pd.DataFrame(total)
        total = total.drop(["_id"], axis=1)
        total = total.dropna()
        total = total.values.tolist()
        arr = []

        for row in total:
            iots = row[0]
            date = row[1]
            atribute = 0
            for iot in iots:
                if iot['name'] == iot_x:
                    for value in iot['values']:
                        if 'values' in value:
                            if value['type'] == 'generation':
                                atribute += value['values']
                            if value['type'] == 'power':
                                atribute += value['values']

            arr.append([date, atribute])

        df = pd.DataFrame(arr, columns=['datetime', 'atribute'])
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S', dayfirst=True)
        df.set_index("datetime", inplace=True)
        df = df.resample('1H').mean()
        df = df.tail(24)
        df['datetime'] = df.index
        return df.values.tolist()

    def change_dr_enable(self, iot, enable):
        self.iot_repo.change_dr_enable(iot, enable)

    def update_instructions(self, instructions):
        self.iot_repo.update_instructions(instructions)
    
    def get_instructions(self):
        return self.iot_repo.get_instructions()