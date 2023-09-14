from domain_logic.logging.concrete_logger_observer import ConcreteLoggerObserver
from domain_logic.logging.observer import Observer
from domain_logic.logging.subject import Subject
from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface
from singleton import singleton


@singleton
class CryptoRepo(Subject):
    def __init__(self, crypto_persistence: CryptoPersistenceInterface):
        self.__crypto_persistence = crypto_persistence
        self.__user_crypto_cache = {}
        self.__observers = []
        logger_observer = ConcreteLoggerObserver()
        self.add_observer(logger_observer)

    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        self.notify_observer(
            f"CryptoRepo executing add_crypto_to_user command adding {cryptocurrency.name} to user with id {user_id}..."
        )
        self.__crypto_persistence.add_crypto_to_user(user_id, cryptocurrency)
        self.notify_observer(
            f"CryptoRepo successfully executed add_crypto_to_user command adding {cryptocurrency.name} to user with "
            f"id {user_id}."
        )
        # Clear user's cache when adding new crypto data
        if user_id in self.__user_crypto_cache:
            del self.__user_crypto_cache[user_id]

    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        self.notify_observer(
            f"CryptoRepo executing get_crypto_for_user with id {user_id}..."
        )
        # Check if user's crypto data is cached
        if user_id in self.__user_crypto_cache:
            self.notify_observer(
                f"CryptoRepo successfully executed get_crypto_for_user with id {user_id} from cache"
            )
            return self.__user_crypto_cache[user_id]
        # If not cached, fetch from the database and cache it
        crypto_list = self.__crypto_persistence.get_crypto_for_user(user_id)
        self.notify_observer(
            f"CryptoRepo successfully executed get_crypto_for_user with id {user_id}"
        )
        self.__user_crypto_cache[user_id] = crypto_list
        return crypto_list

    def calculate_total_crypto_value(self, user_id: str) -> float:
        self.notify_observer(
            f"CryptoRepo executing calculate_total_crypto_value for user with id {user_id}..."
        )
        # Check if total value is cached
        if user_id in self.__user_crypto_cache:
            self.notify_observer(
                f"CryptoRepo successfully executed calculate_total_crypto_value for user with id {user_id} from cache"
            )
            return sum(crypto.price for crypto in self.__user_crypto_cache[user_id])
        # If not cached, calculate from the database and cache it
        total_value = self.__crypto_persistence.calculate_total_crypto_value(user_id)
        self.notify_observer(
            f"CryptoRepo successfully executed calculate_total_crypto_value for user with id {user_id}."
        )
        self.__user_crypto_cache[user_id] = total_value
        return total_value

    def add_observer(self, o: Observer):
        if o not in self.__observers:
            self.__observers.append(o)

    def remove_observer(self, o: Observer):
        if o in self.__observers:
            self.__observers.remove(o)

    def notify_observer(self, message: str):
        for o in self.__observers:
            o.update(message)
