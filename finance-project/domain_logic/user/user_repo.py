from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface
from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.user.user import User
from domain_logic.user.user_persistence_interface import UserPersistenceInterface
from persistence.CryptoPersistenceSqlite import CryptoSqlite


class NonExistingUserId(Exception):
    pass


class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        self.__user_list = None
        self.__persistence = persistence
        self.__crypto_persistence = CryptoRepo(CryptoSqlite("main_users.db"))

    def get_all(self) -> list[User]:
        self.__check_we_have_users()
        return self.__user_list

    def add(self, user: User):
        self.__check_we_have_users()
        self.__persistence.add(user)
        self.__user_list.append(user)

    def get_by_id(self, user_id: str) -> User:
        self.__check_if_user_id_exists(user_id)
        for user in self.__user_list:
            if str(user.id) == user_id:
                crypto_list = self.__crypto_persistence.get_crypto_for_user(
                    str(user.id)
                )
                try:
                    return User(
                        uuid=user.id, username=user.username, crypto=crypto_list
                    )
                except Exception as e:
                    print("CEVA NU E IN ORDINE" + str(e))

    def update(self, user_id: str, username: str):
        self.__check_we_have_users()
        self.__check_if_user_id_exists(user_id)
        self.__persistence.update(user_id, username)
        self.__user_list = self.__persistence.get_all()

    def delete(self, user_id: str):
        self.__check_we_have_users()
        self.__check_if_user_id_exists(user_id)
        self.__persistence.delete(user_id)
        self.__user_list = self.__persistence.get_all()

    def __check_if_user_id_exists(self, user_id):
        self.__check_we_have_users()
        if user_id not in [str(x.id) for x in self.__user_list]:
            raise NonExistingUserId(f"User with id {user_id} does not exist!")

    def __check_we_have_users(self):
        if self.__user_list is None:
            self.__user_list = self.__persistence.get_all()
