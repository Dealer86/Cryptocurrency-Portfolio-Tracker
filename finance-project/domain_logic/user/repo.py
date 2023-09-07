from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.user.user import User
from domain_logic.user.user_persistence_interface import UserPersistenceInterface
from domain_logic.command_logging_observer_pattern.subject import Subject
from domain_logic.command_logging_observer_pattern.observer import Observer
from domain_logic.command_logging_observer_pattern.concrete_logger_observer import ConcreteLoggerObserver
from configuration.config import set_crypto_persistence_type


class NonExistingUserId(Exception):
    pass


class UserAlreadyAdded(Exception):
    pass


class UserRepo(Subject):
    def __init__(self, persistence: UserPersistenceInterface):
        self.__user_list = None
        self.__persistence = persistence
        crypto_persistence_type = set_crypto_persistence_type(
            "configuration/config.json"
        )
        self.__crypto_persistence = CryptoRepo(crypto_persistence_type)
        self.__observers = []
        logger_observer = ConcreteLoggerObserver()
        self.add_observer(logger_observer)

    def get_all(self) -> list[User]:
        self.notify_observer("UserRepo executing get_all command...")
        self.__check_we_have_users()
        self.notify_observer("UserRepo successfully executed get_all command.")
        return self.__user_list

    def add(self, user: User):
        self.notify_observer(
            f"UserRepo executing add command for user {user.username} and id {str(user.id)}..."
        )
        self.__check_we_have_users()
        if user.username in [u.username for u in self.__persistence.get_all()]:
            self.notify_observer(
                f"User with username {user.username} is already taken. Try another username"
            )
            raise UserAlreadyAdded(
                f"User with username {user.username} is already taken. Try another username"
            )
        self.__persistence.add(user)
        self.__user_list.append(user)
        self.notify_observer(
            f"UserRepo successfully executed add command for user {user.username} and id {str(user.id)}"
        )

    def get_by_id(self, user_id: str) -> User:
        self.notify_observer(
            f"UserRepo executing get_by_id command for user with id {user_id}..."
        )
        self.__check_if_user_id_exists(user_id)
        for user in self.__user_list:
            if str(user.id) == user_id:
                crypto_list = self.__crypto_persistence.get_crypto_for_user(
                    str(user.id)
                )
                try:
                    self.notify_observer(
                        f"UserRepo successfully executed get_by_id command for user with id {user_id}"
                    )
                    return User(
                        uuid=user.id, username=user.username, crypto=crypto_list
                    )
                except Exception as e:
                    self.notify_observer("Could not return user. Reason: " + str(e))
                    raise e

    def update(self, user_id: str, username: str):
        self.notify_observer(
            f"UserRepo executing update command for user with id {user_id} and username {username}..."
        )
        self.__check_if_user_id_exists(user_id)
        self.__persistence.update(user_id, username)
        self.notify_observer(
            f"UserRepo successfully executed update command for user with id {user_id} and username {username}.  Refreshing cache."
        )
        self.__user_list = self.__persistence.get_all()

    def delete(self, user_id: str):
        self.notify_observer(
            f"UserRepo executing delete command for user with id {user_id}"
        )
        self.__check_if_user_id_exists(user_id)
        self.__persistence.delete(user_id)
        self.notify_observer(
            f"UserRepo successfully executed delete command for user with id {user_id}. Refreshing cache."
        )
        self.__user_list = self.__persistence.get_all()

    def add_observer(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observer(self, message: str):
        for observer in self.__observers:
            observer.update(message)

    def __check_if_user_id_exists(self, user_id):
        self.__check_we_have_users()
        if user_id not in [str(x.id) for x in self.__user_list]:
            self.notify_observer(f"User with id {user_id} does not exist!")
            raise NonExistingUserId(f"User with id {user_id} does not exist!")

    def __check_we_have_users(self):
        if self.__user_list is None:
            self.__user_list = self.__persistence.get_all()
