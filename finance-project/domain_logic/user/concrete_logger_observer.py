from domain_logic.user.observer import Observer
from domain_logic.user.user import User

import logging


class ConcreteLoggerObserver(Observer):

    def logging_user_added(self, user: User):
        logging.info(f"User added with id {user.id} and username {user.username}")

    def logging_user_removed(self, user_id: str):
        logging.info(f"User with id {user_id} was removed")

    def logging_user_update(self, user_id: str, username: str):
        logging.info(f"User with id {user_id} has updated username to {username}")

    def logging_for_get_by_id(self, user_id: str):
        logging.info(f"Get request for user with id {user_id}")
