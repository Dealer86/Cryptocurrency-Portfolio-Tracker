from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.user.user import User
from domain_logic.user.user_persistence_interface import UserPersistenceInterface
from persistence.CryptoPersistenceSqlite import CryptoSqlite
from domain_logic.user.subject import Subject
from domain_logic.user.observer import Observer
from domain_logic.user.concrete_logger_observer import ConcreteLoggerObserver
from configuration.config import set_crypto_persistence_type
class NonExistingUserId(Exception):
    pass


class UserRepo(Subject):
    def __init__(self, persistence: UserPersistenceInterface):
        self.__user_list = None
        self.__persistence = persistence
        crypto_persistence_type = set_crypto_persistence_type("configuration/config.json")
        self.__crypto_persistence = CryptoRepo(crypto_persistence_type)
        self.__observers = []
        logger_observer = ConcreteLoggerObserver()
        self.add_observer(logger_observer)

    def add_observer(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observer_for_adding_user(self, user: User):
        for o in self.__observers:
            o.logging_user_added(user)

    def notify_observer_for_updating_username(self, user_id: str, username: str):
        for o in self.__observers:
            o.logging_user_update(user_id, username)

    def notify_observer_for_removing_user(self, user_id: str):
        for o in self.__observers:
            o.logging_user_removed(user_id)

    def notify_observer_for_get_by_id(self, user_id: str):
        for o in self.__observers:
            o.logging_for_get_by_id(user_id)

    def get_all(self) -> list[User]:
        self.__check_we_have_users()
        return self.__user_list

    def add(self, user: User):
        self.__check_we_have_users()
        self.__persistence.add(user)
        self.__user_list.append(user)
        self.notify_observer_for_adding_user(user)

    def get_by_id(self, user_id: str) -> User:
        self.__check_if_user_id_exists(user_id)
        for user in self.__user_list:
            if str(user.id) == user_id:
                crypto_list = self.__crypto_persistence.get_crypto_for_user(
                    str(user.id)
                )
                try:
                    self.notify_observer_for_get_by_id(user_id)
                    return User(
                        uuid=user.id, username=user.username, crypto=crypto_list
                    )
                except Exception as e:
                    print("CEVA NU E IN ORDINE" + str(e))


    def update(self, user_id: str, username: str):
        self.__check_if_user_id_exists(user_id)
        self.__persistence.update(user_id, username)
        self.notify_observer_for_updating_username(user_id, username)
        self.__user_list = self.__persistence.get_all()


    def delete(self, user_id: str):
        self.__check_if_user_id_exists(user_id)
        self.__persistence.delete(user_id)
        self.notify_observer_for_removing_user(user_id)
        self.__user_list = self.__persistence.get_all()

    def __check_if_user_id_exists(self, user_id):
        self.__check_we_have_users()
        if user_id not in [str(x.id) for x in self.__user_list]:
            raise NonExistingUserId(f"User with id {user_id} does not exist!")

    def __check_we_have_users(self):
        if self.__user_list is None:
            self.__user_list = self.__persistence.get_all()
