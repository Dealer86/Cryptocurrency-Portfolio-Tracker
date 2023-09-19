import uuid

from exceptions.exceptions import InvalidUsername
from domain_logic.user.user import User


class UserFactory:
    @classmethod
    def make(cls, username: str) -> User:
        cls.__validate_username(username)
        cls.__validate_is_alpha_numeric(username)
        cls.__validate_no_prohibited_words(username)
        user_id = uuid.uuid4()

        return User(user_id, username)

    @classmethod
    def __validate_username(cls, username: str):
        if not (4 < len(username) < 20):
            raise InvalidUsername("Username must be between 4 and 20 chars")

    @classmethod
    def __validate_is_alpha_numeric(cls, username: str):
        if not username.isalnum():
            raise InvalidUsername("Username must be alpha numeric!")

    @classmethod
    def __validate_no_prohibited_words(cls, username: str):
        prohibited_words = ["admin", "password", "superuser", "guest"]
        if username.lower() in prohibited_words:
            raise InvalidUsername(
                "Username must not contain prohibited words like admin, etc."
            )
