from abc import ABC, abstractmethod

from domain_logic.crypto.crypto import Crypto


class CryptoPersistenceInterface(ABC):
    @abstractmethod
    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        pass

    @abstractmethod
    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        pass

    @abstractmethod
    def calculate_total_crypto_value(self, user_id: str) -> float:
        pass
