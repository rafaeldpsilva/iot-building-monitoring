from datetime import datetime, timedelta

from pymongo import MongoClient

from utils import utils


class DemandResponseRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.DEMANDRESPONSE = self.config['storage']['local']['demand_response']
        self.BALANCE = self.config['storage']['local']['balance']
        self.BENEFIT = self.config['storage']['local']['benefit']
        self.CONFIG = self.config['storage']['local']['config']

    def get_auto_answer_config(self):
        client = MongoClient(self.server + ':' + self.port)
        config = list(client[self.CONFIG[0]][self.CONFIG[1]].find())
        client.close()
        if len(config) == 0:
            if self.config['app']['dr_events_auto_accept']:
                auto_answer = {"config": "config", "auto_answer": True}
            else:
                auto_answer = {"config": "config", "auto_answer": False}
            client = MongoClient(self.server + ':' + self.port)
            client[self.CONFIG[0]][self.CONFIG[1]].insert_one(auto_answer)
            client.close()
        else:
            return config[0]['auto_answer']

    def set_auto_answer_config(self, auto_answer):
        if auto_answer:
            print("AUTO ANSWER SET TO TRUE")
        else:
            print("AUTO ANSWER SET TO FALSE")
        client = MongoClient(self.server + ':' + self.port)
        client[self.CONFIG[0]][self.CONFIG[1]].update_one({'config': "config"}, {'$set': {'auto_answer': auto_answer}})
        client.close()

    def get_unanswered_invitations(self):
        client = MongoClient(self.server + ':' + self.port)
        inv = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find({'response': "WAITING"}))
        client.close()
        invitations = []
        for invite in inv:
            event_time = datetime.strftime(invite['event_time'], "%Y-%m-%d %H:%M:%S")
            invitations.append(
                {"datetime": invite['datetime'], "event_time": event_time, "load_kwh": invite['load_kwh'],
                 "load_percentage": invite['load_percentage'], "iots": invite['iots'], "response": invite['response']})
        return invitations

    def get_answered_invitations(self):
        client = MongoClient(self.server + ':' + self.port)
        inv = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find({'response': {"$ne": "WAITING"}}).sort(
            "event_time", -1).limit(5))
        client.close()
        invitations = []
        for invite in inv:
            event_time = datetime.strftime(invite['event_time'], "%Y-%m-%d %H:%M:%S")
            invitations.append(
                {"datetime": invite['datetime'], "event_time": event_time, "load_kwh": invite['load_kwh'],
                 "load_percentage": invite['load_percentage'], "iots": invite['iots'], "response": invite['response']})
        return invitations

    def get_accepted_upcoming_invitations(self):
        client = MongoClient(self.server + ':' + self.port)
        inv = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find(
            {'response': {"$eq": "YES"}, 'event_time': {'$gt': datetime.now() - timedelta(hours=1)}}))
        client.close()
        return inv

    def get_all_invitations(self):
        client = MongoClient(self.server + ':' + self.port)
        invitations = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find())
        client.close()
        return invitations

    def get_invitation(self, event_time):
        client = MongoClient(self.server + ':' + self.port)
        invitation = list(client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].find({'event_time': event_time}))
        client.close()
        return invitation

    def answer_invitation(self, event_time, response):
        res = "NO"
        if response == "YES":
            res = "YES"

        client = MongoClient(self.server + ':' + self.port)
        client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].update_one({'event_time': event_time},
                                                                          {'$set': {'response': res}})
        client.close()
        return response

    def insert_invitation(self, datetime, event_time, load_kwh, load_percentage, iots):
        response = "WAITING"
        if self.get_auto_answer_config():
            response = "YES"

        try:
            invitation = {"datetime": datetime, "event_time": event_time, "load_kwh": load_kwh,
                          "load_percentage": load_percentage, "iots": iots, "response": response}
            client = MongoClient(self.server + ':' + self.port)
            client[self.DEMANDRESPONSE[0]][self.DEMANDRESPONSE[1]].insert_one(invitation)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nInvitation\n', invitation)
