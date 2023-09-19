import os
import unittest

from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_repo import CryptoRepo
from domain_logic.logging.concrete_logger_observer import ConcreteLoggerObserver
from domain_logic.user.user_factory import UserFactory
from persistence.crypto_persistence_file import CryptoPersistenceFile
from persistence.user_persistence_file import UserPersistenceFile


class CryptoRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = "test_repo_data.json"

        crypto_persistence = CryptoPersistenceFile(self.filename)
        self.crypto_repo = CryptoRepo(crypto_persistence)
        self.user_repo = UserPersistenceFile(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_it_gets_empty_list_if_user_has_no_crypto(self):
        # set up
        user = UserFactory.make("JohnDoe")
        self.user_repo.add(user)

        # execution
        user1_assets = self.crypto_repo.get_crypto_for_user(str(user.id))

        # assertion
        self.assertEqual(len(user1_assets), 0)

    def test_it_adds_crypto_to_user(self):
        # set up
        user1 = UserFactory.make("JohnD")
        crypto = Crypto("bitcoin", "btc", 200, "01-01-2023", 1)
        self.user_repo.add(user1)

        # execution
        self.crypto_repo.add_crypto_to_user(str(user1.id), crypto)
        crypto = self.crypto_repo.get_crypto_for_user(str(user1.id))

        # assertion
        self.assertEqual(len(crypto), 1)
        self.assertEqual(crypto[0].name, "bitcoin")
        self.assertEqual(crypto[0].units, 1)

    def test_it_calculates_crypto_value_for_a_specific_user(self):
        # set up
        user2 = UserFactory.make("JohnD")
        crypto = Crypto("bitcoin", "btc", 200, "01-01-2023", 1)
        crypto2 = Crypto("ethereum", "eth", 150, "01-01-2023", 1)
        self.user_repo.add(user2)
        self.crypto_repo.add_crypto_to_user(str(user2.id), crypto)
        self.crypto_repo.add_crypto_to_user(str(user2.id), crypto2)

        # execution
        actual_value = self.crypto_repo.calculate_total_crypto_value(str(user2.id))
        expected_value = 350

        # assertion
        self.assertEqual(actual_value, expected_value)

    def test_it_add_observer(self):
        # set up
        logger_observer = ConcreteLoggerObserver()

        # execution
        self.crypto_repo.add_observer(logger_observer)
        observers = self.crypto_repo.observers
        # assertion
        self.assertIn(logger_observer, observers)

    def test_it_removes_observer(self):
        # set up
        logger_observer = ConcreteLoggerObserver()
        self.crypto_repo.add_observer(logger_observer)

        # execution
        self.crypto_repo.remove_observer(logger_observer)
        observers = self.crypto_repo.observers

        # assertion
        self.assertNotIn(logger_observer, observers)


if __name__ == "__main__":
    unittest.main()
