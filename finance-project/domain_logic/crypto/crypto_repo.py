import sqlite3

from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface
from domain_logic.crypto.external_crypto_api_interface import ExternalCryptoApiInterface


class CryptoRepo:
    def __init__(self, persistence: CryptoPersistenceInterface, external_api: ExternalCryptoApiInterface):
        self.__external_api = external_api
        self.__persistence = persistence
        self.__user_crypto_cache = {}

    def use_external_api(self, coin_id: str, start_date: str = "2023-01-01", end_date: str = "2023-07-28"):
        return self.__external_api.get_cryptocurrency_price_history(coin_id, start_date, end_date)

    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        self.__persistence.add_crypto_to_user(user_id, cryptocurrency)
        # Clear user's cache when adding new crypto data
        if user_id in self.__user_crypto_cache:
            del self.__user_crypto_cache[user_id]

    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        # Check if user's crypto data is cached
        if user_id in self.__user_crypto_cache:
            return self.__user_crypto_cache[user_id]
        # If not cached, fetch from the database and cache it
        crypto_list = self.__persistence.get_crypto_for_user(user_id)
        self.__user_crypto_cache[user_id] = crypto_list
        return crypto_list

    def calculate_total_crypto_value(self, user_id: str) -> float:
        # Check if total value is cached
        if user_id in self.__user_crypto_cache:
            return sum(crypto.price for crypto in self.__user_crypto_cache[user_id])
        # If not cached, calculate from the database and cache it
        total_value = self.__persistence.calculate_total_crypto_value(user_id)
        self.__user_crypto_cache[user_id] = total_value
        return total_value
