from database.P2PRepository import P2PRepository
from datetime import datetime, timedelta

class P2PService:
    def __init__(self):
        self.p2p_repo = P2PRepository()

    def update_prices(self, sell_percentage, buy_percentage):
        self.p2p_repo.update_prices(sell_percentage, buy_percentage)
        return True

    def get_prices(self):
        prices = self.p2p_repo.get_prices()
        return prices
    
    def set_transaction(self, hour, peer, quantity, cost):
        t = datetime.now().replace(hour=hour,minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.p2p_repo.set_transaction(t, peer, quantity, cost)
