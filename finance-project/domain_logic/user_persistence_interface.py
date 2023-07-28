from abc import ABC, abstractmethod

from domain_logic.user import User


class UserPersistenceInterface(ABC):

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass

    @abstractmethod
    def update(self, user_id: str, username: str):
        pass
