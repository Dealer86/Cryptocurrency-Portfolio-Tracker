from uuid import UUID

from domain_logic.crypto.crypto import Crypto


class User:
    def __init__(self, uuid: UUID, username: str, crypto: list[Crypto] = None):
        self.__id = uuid
        self.__username = username
        self.__crypto = crypto if crypto else []

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def crypto(self) -> list[Crypto]:
        return self.__crypto
