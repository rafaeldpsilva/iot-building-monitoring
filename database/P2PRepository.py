from datetime import datetime

from pymongo import MongoClient

from utils import utils


class P2PRepository:
    def __init__(self):
        self.config = utils.get_config()
        self.server = str(self.config['storage']['local']['server'])
        self.port = str(self.config['storage']['local']['port'])
        self.P2P_PRICES = self.config['storage']['local']['p2p_prices']

    def update_prices(self, sell_percentage, buy_percentage):
        try:
            prices = {"datetime": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                      "sell_percentage": sell_percentage, "buy_percentage": buy_percentage}
            client = MongoClient(self.server + ':' + self.port)
            client[self.P2P_PRICES[0]][self.P2P_PRICES[1]].insert_one(prices)
        except Exception as e:
            print("An exception occurred ::", e)
        finally:
            client.close()

        if self.config['app']['monitoring']:
            print('\nP2P Prices\n', prices)

    def get_prices(self):
        client = MongoClient(self.server + ':' + self.port)
        prices = list(
            client[self.P2P_PRICES[0]][self.P2P_PRICES[1]].find().sort("datetime", -1))
        client.close()
        if len(prices) == 0:
            buy_per = 0.10
            sell_per = 0.12
        else:
            buy_per = prices[0]['buy_percentage']
            sell_per = prices[0]['sell_percentage']
        market_prices = utils.update_values_get('market prices', 'http://192.168.2.68:5000/today')['price']
        buy = []
        sell = []
        for price in market_prices:
            print(price)
            buy.append(price[1] * (1 - buy_per))
            sell.append(price[1] * (1 + sell_per))

        return {'buy': buy, 'sell': sell, 'market_prices': market_prices}
