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

    @username.setter
    def username(self, new_username: str):
        self.__username = new_username

    @property
    def crypto(self) -> list[Crypto]:
        return self.__crypto

    @classmethod
    def from_dict(cls, d: dict):

        return User(uuid=d["id"], username=d["username"], crypto=[Crypto.from_dict(x) for x in d["crypto"]])

    def to_dict(self):
        crypto_dict = [Crypto.to_dict(x) for x in self.__crypto]
        return {"id": str(self.__id), "username": self.__username, "crypto": crypto_dict}

