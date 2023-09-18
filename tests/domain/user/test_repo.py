import os
import unittest

from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.logging.concrete_logger_observer import ConcreteLoggerObserver
from domain_logic.user.repo import UserRepo
from domain_logic.user.user_factory import UserFactory

from persistence.crypto_persistence_file import CryptoPersistenceFile
from persistence.user_persistence_file import UserPersistenceFile


class UserRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        user_file = UserPersistenceFile("test_users.json")
        crypto_file = CryptoPersistenceFile("test_users.json")

        crypto_repo = CryptoRepo(crypto_file)
        self.user_repo = UserRepo(user_file, crypto_repo)
        username = "random"
        self.new_user = UserFactory.make(username)

    def test_get_all_gets_empty_list_if_database_is_empty(self):
        # execution
        all_users = self.user_repo.get_all()

        # assertion
        self.assertEqual([], all_users)

    def test_it_adds_a_user(self):
        # execution
        self.user_repo.add(self.new_user)
        actual_new_user = self.user_repo.get_all()

        # assertion
        self.assertIn(self.new_user, actual_new_user)

    def test_it_gets_a_user_by_id(self):
        # set up
        self.user_repo.add(self.new_user)
        # execution
        actual_user = self.user_repo.get_by_id(str(self.new_user.id))

        # assertion
        self.assertEqual("random", actual_user.username)

    def test_it_delete_a_user(self):
        # set up
        self.user_repo.add(self.new_user)

        # execution
        self.user_repo.delete(str(self.new_user.id))
        all_users = self.user_repo.get_all()

        # assertion
        self.assertNotIn(self.new_user.username, all_users)

    def test_it_updates_a_user(self):
        # set up
        self.user_repo.add(self.new_user)

        # execution
        actual_new_username = "newname"
        self.user_repo.update(str(self.new_user.id), actual_new_username)
        all_usernames = [u.username for u in self.user_repo.get_all()]

        # assertion
        self.assertIn(actual_new_username, all_usernames)

    def test_it_add_observer(self):
        # set up
        logger_observer = ConcreteLoggerObserver()

        # execution
        self.user_repo.add_observer(logger_observer)
        observers = self.user_repo.observers
        # assertion
        self.assertIn(logger_observer, observers)

    def test_it_removes_observer(self):
        # set up
        logger_observer = ConcreteLoggerObserver()
        self.user_repo.add_observer(logger_observer)

        # execution
        self.user_repo.remove_observer(logger_observer)
        observers = self.user_repo.observers

        # assertion
        self.assertNotIn(logger_observer, observers)

    def tearDown(self) -> None:
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()
