class Crypto:
    def __init__(
        self, name: str, symbol: str, price: float, last_updated: str, units: float
    ):
        self.__name = name
        self.__symbol = symbol
        self.__price = price
        self.__last_updated = last_updated
        self.__units = units

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

    @property
    def units(self):
        return self.__units

    @classmethod
    def from_dict(cls, d: dict):
        return Crypto(
            name=d["name"],
            symbol=d["symbol"],
            price=d["price"],
            last_updated=d["last_updated"],
            units=d["units"]
        )

    def to_dict(self):
        return {
            "name": self.__name,
            "symbol": self.__symbol,
            "price": self.__price,
            "last_updated": self.__last_updated,
            "units": self.__units
        }
