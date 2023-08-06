from domain_logic.user.user import User
import json
import os

from domain_logic.user.user_persistence_interface import UserPersistenceInterface


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:
        if not os.path.exists(self.__file_path):
            return []
        with open(self.__file_path) as file:
            data = file.read()
        data_info = json.loads(data)
        return [User.from_dict(x) for x in data_info]

    def add(self, user: User):
        user_list = self.get_all()
        user_list.append(user)
        self.save_to_file(user_list)

    def update(self, user_id: str, username: str):
        user_list = self.get_all()
        for u in user_list:
            if u.id == user_id:
                u.username = username
        self.save_to_file(user_list)

    def delete(self, user_id: str):
        user_list = self.get_all()
        user_list = [u for u in user_list if u.id != user_id]
        self.save_to_file(user_list)

    def save_to_file(self, list_of_user: list[User]):
        data = [User.to_dict(x) for x in list_of_user]
        prep_data = json.dumps(data, indent=4)
        with open(self.__file_path, "w") as file:
            file.write(prep_data)


