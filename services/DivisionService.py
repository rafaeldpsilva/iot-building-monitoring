from datetime import datetime, timedelta

import pandas as pd

from database.BuildingRepository import BuildingRepository
from database.DivisionRepository import DivisionRepository
from model.Division import Division


class DivisionService:
    def __init__(self):
        self.divisions_repo = DivisionRepository()

    def get_ac_status(self, id):
        division = self.get_division(id)

        building_repo = BuildingRepository()
        df = pd.DataFrame(building_repo.get_historic(datetime.now() - timedelta(hours=1)))
        df = df.drop("_id", axis=1)

        return division.get_ac_status(df)

    def get_divisions(self):
        divisions_list = self.divisions_repo.get_divisions()
        divisions = []
        for div in divisions_list:
            division = Division(div['name'], div['iots'], str(div['_id']), div['ac_status_configuration'])
            divisions.append(division.to_json())
        return divisions

    def insert_division(self, name, iots):
        division = Division(name, iots)
        division.save()

    def update_division(self, id, name, iots, ac_status_configuration):
        division = self.get_division(id)
        division.update(name, iots, ac_status_configuration)

    def get_division(self, id):
        division_repo = DivisionRepository()
        div = division_repo.get_division(id)
        return Division(div['name'], div['iots'], div['_id'], div['ac_status_configuration'])
