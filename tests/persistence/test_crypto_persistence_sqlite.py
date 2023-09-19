import os
import sqlite3
import unittest

from domain_logic.crypto.crypto import Crypto
from domain_logic.user.user_factory import UserFactory
from persistence.crypto_persistence_sqlite import CryptoSqlite
from persistence.user_persistence_sqlite import UserPersistenceSqlite


class CryptoSqliteTestCase(unittest.TestCase):
    def setUp(self):
        self.crypto_persistence = CryptoSqlite("test_data.db")
        self.user_repo = UserPersistenceSqlite("test_data.db")

    def test_it_gets_empty_list_if_user_has_no_crypto(self):
        # set up
        user = UserFactory.make("JohnDoe")
        self.user_repo.add(user)

        # execution
        user1_assets = self.crypto_persistence.get_crypto_for_user(str(user.id))

        # assertion
        self.assertEqual(len(user1_assets), 0)

    def test_it_adds_crypto_to_user(self):
        # set up
        user1 = UserFactory.make("JohnD")
        crypto = Crypto("bitcoin", "btc", 200, "01-01-2023", 1)
        self.user_repo.add(user1)

        # execution
        self.crypto_persistence.add_crypto_to_user(str(user1.id), crypto)
        crypto = self.crypto_persistence.get_crypto_for_user(str(user1.id))

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
        self.crypto_persistence.add_crypto_to_user(str(user2.id), crypto)
        self.crypto_persistence.add_crypto_to_user(str(user2.id), crypto2)

        # execution
        actual_value = self.crypto_persistence.calculate_total_crypto_value(
            str(user2.id)
        )
        expected_value = 350

        # assertion
        self.assertEqual(actual_value, expected_value)

    @classmethod
    def tearDownClass(cls) -> None:
        with sqlite3.connect("test_data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE users")


if __name__ == "__main__":
    unittest.main()
