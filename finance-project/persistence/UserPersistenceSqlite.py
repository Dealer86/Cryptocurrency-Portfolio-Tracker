import sqlite3
from domain_logic.user.user import User
from domain_logic.user.user_persistence_interface import UserPersistenceInterface


class UserPersistenceSqlite(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users")

            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
                else:
                    raise e
            users_info = cursor.fetchall()
            users = [User(uuid=x[0], username=x[1]) for x in users_info]
            return users

    def add(self, user: User):
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users VALUES (?, ?)", (str(user.id), user.username)
                )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    cursor.execute(
                        "CREATE TABLE users(id TEXT PRIMARY KEY NOT NULL, username TEXT NOT NULL)"
                    )
                    cursor.execute(
                        "INSERT INTO users VALUES (?, ?)", (str(user.id), user.username)
                    )
                else:
                    raise e
            conn.commit()

    def delete(self, user_id: str):
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM users WHERE id= (?)", (user_id,))
            except sqlite3.OperationalError as e:
                raise e
            conn.commit()

    def update(self, user_id: str, username: str):
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"UPDATE users SET username = '{username}' WHERE id = '{user_id}'"
                )
            except sqlite3.OperationalError as e:
                raise e
            conn.commit()
