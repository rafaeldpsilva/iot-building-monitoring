from pymongo import MongoClient
from datetime import datetime
from utils import utils


class DemandResponseRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.DEMANDRESPONSE = self.config['storage']['local']['demand_response']

    def get_invitations(self):
        client = MongoClient(self.server + ':' + self.port)
        invitations = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find())
        client.close()
        return invitations
    
    def get_invitation(self, event_time):
        client = MongoClient(self.server + ':' + self.port)
        invitation = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find({'event_time': event_time } ))
        client.close()
        return invitation
    
    def answer_invitation(self, event_time, response):
        response = "NO"
        if response:
            response = "YES"

        client = MongoClient(self.server + ':' + self.port)
        client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].update_one({'event_time': event_time},{'$set': { 'response': response}})
        client.close()
        return response
    
    def insert_invitation(self, datetime, event_time, load_kwh, load_percentage):
        response = "WAITING"
        if self.config['app']['dr_events_auto_accept']:
            response = "YES"
        
        try:
            invitation = {"datetime": datetime, "event_time": event_time, "load_kwh": load_kwh, "load_percentage": load_percentage, "response": response}
            client = MongoClient(self.server + ':' + self.port)
            client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].insert_one(invitation)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nInvitation\n',invitation)
