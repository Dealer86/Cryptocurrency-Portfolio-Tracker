import json

from persistence.CryptoPersistenceSqlite import CryptoSqlite
from persistence.UserPersistenceSqlite import UserPersistenceSqlite
from persistence.crypto_persistence_file import CryptoPersistenceFile
from persistence.user_persistence_file import UserPersistenceFile


class InvalidDataBase(Exception):
    pass


def set_user_persistence_type(file_path: str):
    with open(file_path) as file:
        data = file.read()
        user_config_choice = json.loads(data)
        if user_config_choice.get("persistence") == "json":
            return UserPersistenceFile("main_users.json")
        elif user_config_choice.get("persistence") == "sqlite":
            return UserPersistenceSqlite("main_users.db")
        else:
            raise InvalidDataBase("Config must be json or sqlite, be sure it is properly specified in config.json")


def set_crypto_persistence_type(file_path: str):
    with open(file_path) as file:
        data = file.read()
        user_config_choice = json.loads(data)
        if user_config_choice.get("persistence") == "json":
            return CryptoPersistenceFile("main_users.json")
        elif user_config_choice.get("persistence") == "sqlite":
            return CryptoSqlite("main_users.db")
        else:
            raise InvalidDataBase("Config must be json or sqlite, be sure it is properly specified in config.json")
