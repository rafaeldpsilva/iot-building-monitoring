from database.P2PRepository import P2PRepository


class P2PService:
    def __init__(self):
        self.p2p_repo = P2PRepository()

    def update_prices(self, sell_percentage, buy_percentage):
        self.p2p_repo.update_prices(sell_percentage, buy_percentage)
        return True

    def get_prices(self):
        prices = self.p2p_repo.get_prices()
        return prices
