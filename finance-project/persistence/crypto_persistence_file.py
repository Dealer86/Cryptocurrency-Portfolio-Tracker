from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface
from persistence.user_persistence_file import UserPersistenceFile


class CryptoPersistenceFile(CryptoPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.user_persistence_file = UserPersistenceFile(self.__file_path)

    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):

        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if str(u.id) == user_id:
                u.crypto.append(cryptocurrency)
        self.user_persistence_file.save_to_file(user_list)

    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if str(u.id) == user_id:
                return u.crypto

    def calculate_total_crypto_value(self, user_id: str) -> float:
        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if u.id == user_id:
                data = u.crypto
                total_value = 0
                for d in data:
                    total_value += d.price
                return total_value


