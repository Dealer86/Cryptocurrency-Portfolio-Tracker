from abc import ABC, abstractmethod


class ExternalCryptoApiInterface(ABC):
    @classmethod
    @abstractmethod
    def get_cryptocurrency_price_history(
        cls, coin_id: str, start_date: str = "2023-01-01", end_date: str = "2023-07-28"
    ):
        pass
