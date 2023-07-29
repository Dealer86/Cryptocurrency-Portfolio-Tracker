
import uuid

from domain_logic.user.user import User


class InvalidUsername(Exception):
    pass


class UserFactory:
    @classmethod
    def make(cls, username: str) -> User:
        cls.__validate_username(username)
        user_id = uuid.uuid4()

        return User(user_id, username)

    @classmethod
    def __validate_username(cls, username: str):
        if not (4 < len(username) < 20):
            raise InvalidUsername("Username must be between 4 and 20 chars")

