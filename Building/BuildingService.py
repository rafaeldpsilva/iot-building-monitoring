from Building.BuildingRepository import BuildingRepository

class BuildingService:
    def __init__(self):
        self.building_repo = BuildingRepository()

    def protected_energy(TM):
        consumption = []
    
        if TM.dados['Data Aggregation'] == 'individual':
            for i in TM.dados['List of Resources']:
                for iot in cr.iots:
                    if i['text'] == iot.name and i['text'] != 'Generation':
                        consumption.append({"resource": iot.name, "values": iot.getPower()})
                    
                    if i['text'] == iot.name and i['text'] == 'Generation':
                        consumption.append({"resource": iot.name, "values": iot.getGeneration()})
        else:
            consumption = {"resource": "end-user", "values": 0}
            for i in TM.dados['List of Resources']:
                for iot in cr.iots:
                    if i['text'] == iot.name:
                        consumption['values'] += iot.getPower() 
        return consumption

    def protected_historic():
        col = self.building_repo.get_iots_reading_col()
        x = []  #! O QUE É ISTO - X e Y

        time = datetime.datetime.now() - datetime.timedelta(minutes=180) 
        timeemb = datetime.datetime.now() - datetime.timedelta(minutes=int(TM.dados['Embargo Period']))
        
        indexArray = []
        dataArray = []
        columns = []
        if TM.dados['Data Aggregation'] == 'sum':
            columns.append("end-user")
        getIndex = True;
        for i in TM.dados['List of Resources']:
            x = col.find( {"name": i['text'], 'datetime': { '$gt': str(time), '$lt' : str(timeemb)} } )
            y = list(x)
            if TM.dados['Data Aggregation'] == 'individual':
                columns.append(i['text'])
            index = 0
            for entry in y:
                if getIndex:
                    indexArray.append(datetime.datetime.strptime(entry["datetime"][:19], "%Y-%m-%d %H:%M:%S"))
                    dataArray.append([])
                    if TM.dados['Data Aggregation'] == 'sum':
                        dataArray[index].append(0)
                if TM.dados['Data Aggregation'] == 'individual':
                    dataArray[index].append(getvalue(entry['iot_values'], 'power'))
                else:
                    dataArray[index][0] += getvalue(entry['iot_values'], 'power')
                index += 1
            if getIndex:
                getIndex = False

        df = pd.DataFrame(dataArray, index=indexArray, columns=columns)

        if TM.dados["Time Aggregation"] == "5minutes":
            df=df.groupby(df.index.floor('5T')).mean()
        elif TM.dados["Time Aggregation"] == "15minutes":
            df=df.groupby(df.index.floor('15T')).mean()
        elif TM.dados["Time Aggregation"] == "60minutes":
            df=df.groupby(df.index.floor('60T')).mean()

        return df

    def forecast():
        col = self.building_repo.get_forecastvalue_col()
        
        x = col.find().sort("_id", pymongo.DESCENDING).limit(1)
        y = list(x)
        df = pd.DataFrame(y)
        
        df.drop('_id', inplace=True, axis=1)
        # df = df.iloc[1: , :]
        # print(df)
        # df.drop('0', inplace=True, axis=1)
        # df_n = df.set_index('datetime')
        # reversed_df = df_n.iloc[::-1]

        return df