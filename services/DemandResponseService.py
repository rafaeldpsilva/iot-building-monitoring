from datetime import datetime
from database.DemandResponseRepository import DemandResponseRepository
from utils import utils

class DemandResponseService:
    def __init__(self):
        self.dr_repo = DemandResponseRepository()
    
    def get_invitations(self, event_time):
        event_time = datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S")
        invitation = self.dr_repo.get_invitation(event_time)[0]
        return invitation['datetime'],invitation['event_time'],invitation['load_kwh'],invitation['load_percentage'],invitation['response']

    def get_unanswered_invitations(self):
        return self.dr_repo.get_unanswered_invitations()

    def get_answered_invitations(self):
        return self.dr_repo.get_answered_invitations()

    def answer_invitation(self, event_time, response):
        event_time = datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S")
        return self.dr_repo.answer_invitation(event_time,response)

    def invitation(self, event_time, load_kwh, load_percentage, iots):
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_time = datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S")
        return self.dr_repo.insert_invitation(creation_date, event_time, load_kwh, load_percentage, iots)
