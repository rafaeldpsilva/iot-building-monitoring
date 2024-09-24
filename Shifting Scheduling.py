#Inputs
from datetime import datetime

print(datt)
Tariff=pd.DataFrame([0.0923,0.0923,0.0812,0.0812,0.0812,0.0812,0.0923,0.1358,      #00 at 07 am
                          0.1358,0.2164,0.2164,0.2164,0.1358,0.1358,0.1358,0.1358, #08 at 15 am
                          0.1358,0.1358,0.1358,0.1358,0.1358,0.1358,0.1358,0.1358],#16 at 23 am
                          columns = ["Tariff"],
                          index   = ["%01d" %i for i in range(0,24)])

Main_DR_Event   = [11]
#DF to save the data regarding the shifting hours, energy, and cost
Shiftscheduling = pd.DataFrame(float("nan"), columns = ['Total_Shifting_Flex', 'Shifting_Hours', 'Shifting_Flex_perHour', 'Shifting_Flex_Cost'], index = DF_Test.index, dtype="object") # DF_Test.index represents the appliance's ID (e.g. "DD01.1", "DD01.5", "DD01.7", "DD02.2", ..., etc)
Shiftscheduling["Total_Shifting_Flex"] = DF_Test["Shifting_Flex"]

#Shifting Scheduling:
for i in Shiftscheduling.index:
    #List with the hours (e.g. DR event is at 11:00, the list will be [10,12,13] )
    Hours = [Main_DR_Event[0] - 1, Main_DR_Event[0] + 1, Main_DR_Event[0] + 2]

    #First hour is before the event; Second and Third hour represent the 1º and 2º hour after the event
    Shiftscheduling["Shifting_Flex_Cost"][i]    = ((Tariff.Tariff.iloc[Hours][0]*0.25  + Tariff.Tariff.iloc[Hours][1]*0.50  + Tariff.Tariff.iloc[Hours][2]*0.25) * Shiftscheduling["Total_Shifting_Flex"][i])
    Shiftscheduling["Shifting_Hours"][i]        = Hours
    Shiftscheduling["Shifting_Flex_perHour"][i] = [round(v * Shiftscheduling["Total_Shifting_Flex"][i],3) for v in [0.25,0.50,0.25]]