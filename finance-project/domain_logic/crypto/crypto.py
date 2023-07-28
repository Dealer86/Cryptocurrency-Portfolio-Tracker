class Crypto:
    def __init__(self, name: str, symbol: str, price: float, last_updated: str):
        self.__name = name
        self.__symbol = symbol
        self.__price = price
        self.__last_updated = last_updated

    @property
    def name(self):
        return self.__name

    @property
    def symbol(self):
        return self.__symbol

    @property
    def price(self):
        return self.__price

    @property
    def last_updated(self):
        return self.__last_updated
