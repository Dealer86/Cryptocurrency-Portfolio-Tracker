from abc import ABC, abstractmethod

from domain_logic.user.user import User


class Observer(ABC):
    @abstractmethod
    def logging_user_added(self, user: User):
        pass

    @abstractmethod
    def logging_user_removed(self, user_id: str):
        pass

    @abstractmethod
    def logging_user_update(self, user_id: str, username: str):
        pass

    @abstractmethod
    def logging_for_get_by_id(self, user_id: str):
        pass
