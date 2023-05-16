from datetime import datetime
import schedule
import time
from database.DemandResponseRepository import DemandResponseRepository
from services.DemandResponseService import DemandResponseService

dr_repo = DemandResponseRepository()
event_time=datetime.strptime("2023-05-09 18:28:00", "%Y-%m-%d %H:%M:%S")
datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print(dr_repo.insert_invitation(datetime, event_time, '100', '23.6'))
invitates = dr_repo.get_all_invitations()
print(invitates)
invitations = []
for invite in invitates:
    invitations.append([invite['datetime'],invite['event_time'],invite['load_kwh'],invite['load_percentage'],invite['response']])

i = 0
for invite in invitations:
    print("\n\nInvitation",i,"\nDatetime:",invite[0],"\nEvent Time:",invite[1],"\nLoad KWH:",invite[2],"\nLoad Percentage:",invite[3],"\nResponse:",invite[4])
    i += 1

dr_service = DemandResponseService()
print(dr_repo.get_invitation(invitations[1][1]))
print(dr_service.answer_invitation(invitations[1][1], False))
print(dr_repo.get_all_invitations())