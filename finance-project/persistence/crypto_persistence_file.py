import logging
from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface
from exceptions.exceptions import UserNotFound
from persistence.user_persistence_file import UserPersistenceFile


class CryptoPersistenceFile(CryptoPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.user_persistence_file = UserPersistenceFile(self.__file_path)

    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        logging.info(
            f"CryptoPersistenceFile executing add_crypto_to_user command,"
            f"trying to add {cryptocurrency.name} for user with id {user_id}..."
        )
        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if str(u.id) == user_id:
                logging.info(
                    f"CryptoPersistenceFile successfully executed add_crypto_to_user command,"
                    f"adding {cryptocurrency.name} for user with id {user_id}."
                )
                u.crypto.append(cryptocurrency)
                break
        else:
            logging.warning(f"User with id {user_id} not found!")
            raise UserNotFound(f"User with id {user_id} not found!")
        self.user_persistence_file.save_to_file(user_list)

    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        logging.info(
            f"CryptoPersistenceFile executing get_crypto_for_user command, for user with id {user_id}..."
        )
        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if str(u.id) == user_id:
                logging.info(
                    f"CryptoPersistenceFile successfully executed get_crypto_for_user command,"
                    f" for user with id {user_id}..."
                )
                return u.crypto
            else:
                logging.warning(f"User with id {user_id} not found!")
                raise UserNotFound(f"User with id {user_id} not found!")

    def calculate_total_crypto_value(self, user_id: str) -> float:
        logging.info(
            f"CryptoPersistenceFile executing calculate_total_crypto_value command,"
            f" for user with id {user_id}..."
        )
        user_list = self.user_persistence_file.get_all()
        for u in user_list:
            if u.id == user_id:
                data = u.crypto
                total_value = 0
                for d in data:
                    total_value += d.price
                logging.info(
                    f"CryptoPersistenceFile successfully executed calculate_total_crypto_value command,"
                    f" for user with id {user_id}..."
                )
                return total_value
            else:
                logging.warning(f"User with id {user_id} not found!")
                raise UserNotFound(f"User with id {user_id} not found!")
