from database.BuildingRepository import BuildingRepository

building_repo = BuildingRepository()

def get_mean_values( start, main_participants):
    historic = building_repo.get_historic(start)
    instants = 0
    consumption = 0
    generation = 0
    for instant in historic:
        instants += 1
        for iot in instant['iots']:
            event_participant = False
            for part in main_participants:
                if iot['name'] == part:
                    event_participant = True

            for value in iot['values']:
                if 'values' in value:
                    if value['type'] == "power" and not event_participant:
                            consumption += value['values']

                    if iot['type'] == "generation":
                            generation += value['values']
    return consumption/instants, generation/instants

print(get_mean_values("2023-05-30 16:20:00", ['Air Conditioner 101']))