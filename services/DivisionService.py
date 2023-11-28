from database.DivisionRepository import DivisionRepository


class DivisionService:
    def __init__(self):
        self.divisions_repo = DivisionRepository()

    def get_divisions(self):
        return self.divisions_repo.get_divisions()

    def insert_division(self, name, iots):
        # verify if iots exist
        # verify if name is not duplicate
        return self.divisions_repo.insert_division(name, iots)
