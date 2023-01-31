
# TioCPS

## Quickstart

To quickly install all the needed dependencies run:

```
pip install -r reqs.txt
```

To start the application run [`main.py`](/api/main.py)

### Database Access

In order to change the database access you need to change the following files:

[config](./config/config.json) :

```
{
	"storage" : {
		"local" : {
			"type" : "mongodb",
			"server" : "192.168.1.2",
			"port" : 27017,
			"database" : "EXAMPLE"  
		}
	}
}
```

[BuildingRepository](./database/BuildingRepository.py) :

```
self.building_iot_reading = self.client.Building.iots_reading
self.building_forecast =self.client.Forecast.building_forecast_col
self.building_totalpower =self.client.TotalPower.buidling_totalpower_col
```

[TokenRepository](./database/TokenRepository.py) :

```
self.tokensdb = client.Tokens_BUILDING_EXAMPLE.tokencol
```

### Notas Rafael

- criar novo mecanismo para ler configurações (em vez de ler todas as vezes, ler apenas no inicio)
