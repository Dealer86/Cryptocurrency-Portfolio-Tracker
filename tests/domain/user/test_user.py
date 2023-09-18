import unittest
import uuid
from domain_logic.user.user import User
from domain_logic.crypto.crypto import Crypto


class UserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.actual_user_id = uuid.uuid4()
        self.actual_username = "random"
        self.new_user = User(self.actual_user_id, self.actual_username)

        self.new_crypto = Crypto("bitcoin", "btc", 200, "01-01-2023", 0)
        self.new_user_with_crypto = User(
            self.actual_user_id, self.actual_username, [self.new_crypto]
        )

    def test_it_sets_the_id(self):
        self.assertEqual(self.actual_user_id, self.new_user.id)

    def test_it_sets_the_right_username(self):
        self.assertEqual(self.actual_username, self.new_user.username)

    def test_username_setter(self):
        # set up
        actual_username = "random1"

        # execution
        self.new_user.username = actual_username

        # assertion
        self.assertEqual(actual_username, self.new_user.username)

    def test_it_sets_empty_list_if_we_do_not_specify_crypto(self):
        self.assertEqual(self.new_user.crypto, [])

    def test_it_sets_the_cryptocurrency_we_give(self):
        self.assertIn(self.new_crypto, self.new_user_with_crypto.crypto)

    def test_it_returns_a_user_from_a_dictionary(self):
        # set up
        new_dict = {
            "id": self.actual_user_id,
            "username": self.actual_username,
            "crypto": [
                {
                    "name": "bitcoin",
                    "symbol": "btc",
                    "price": 200,
                    "last_updated": "01-01-2023",
                    "units": 0,
                }
            ],
        }

        # execution
        new_user_from_dict = User.from_dict(new_dict)

        # assertion
        self.assertIsInstance(new_user_from_dict, User)

    def test_it_returns_a_dict_from_a_user_object(self):
        # execution
        new_dict = User.to_dict(self.new_user_with_crypto)

        # assertion
        self.assertEqual(type(new_dict), dict)


if __name__ == "__main__":
    unittest.main()
