from domain_logic.user.user import User
import json
import os

from domain_logic.user.user_persistence_interface import UserPersistenceInterface
from exceptions.exceptions import (
    UserFileError,
    UsernameAlreadyExistsException,
    UserNotFound,
)


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:
        if not os.path.exists(self.__file_path):
            return []
        with open(self.__file_path) as file:
            data = file.read()
        try:
            data_info = json.loads(data)
            return [User.from_dict(x) for x in data_info]
        except json.JSONDecodeError as e:
            raise UserFileError(f"Error decoding user data. Reason: {str(e)}")

    def add(self, user: User):
        user_list = self.get_all()
        if user.username in [u.username for u in user_list]:
            raise UsernameAlreadyExistsException(
                f"User with username {user.username} already added. Try another username."
            )
        user_list.append(user)
        self.save_to_file(user_list)

    def update(self, user_id: str, username: str):
        user_list = self.get_all()
        self.__check_if_user_id_exists(user_id, user_list)
        for u in user_list:
            if str(u.id) == user_id:
                u.username = username
        self.save_to_file(user_list)

    def delete(self, user_id: str):
        user_list = self.get_all()
        self.__check_if_user_id_exists(user_id, user_list)
        user_list = [u for u in user_list if u.id != user_id]
        self.save_to_file(user_list)

    def save_to_file(self, list_of_user: list[User]):
        data = [User.to_dict(x) for x in list_of_user]
        prep_data = json.dumps(data, indent=4)
        with open(self.__file_path, "w") as file:
            file.write(prep_data)

    @classmethod
    def __check_if_user_id_exists(cls, user_id, user_list):
        if user_id not in [str(u.id) for u in user_list]:
            raise UserNotFound(f"User with id {user_id} not found.")
