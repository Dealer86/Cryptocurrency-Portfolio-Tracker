import unittest
import random

from domain_logic.user.user import User
from domain_logic.user.user_factory import UserFactory
from exceptions.exceptions import InvalidUsername


class UserFactoryTestCase(unittest.TestCase):
    def test_it_creates_a_user_if_username_is_correct(self):
        # set up
        actual_username = "random"

        # execution
        new_user = UserFactory.make(actual_username)

        # assertion
        self.assertIsInstance(new_user, User)

    def test_it_raises_exception_if_username_is_below_4_chars(self):
        # set up
        actual_username_below_4_chars = "abc"

        # execution
        with self.assertRaises(InvalidUsername) as context:
            UserFactory.make(actual_username_below_4_chars)

        # assertion
        self.assertEqual(
            "Username must be between 4 and 20 chars", str(context.exception)
        )

    def test_it_raises_exception_if_username_is_above_20_chars(self):
        # set up
        actual_username_above_20_chars = "a" * 21

        # execution
        with self.assertRaises(InvalidUsername) as context:
            UserFactory.make(actual_username_above_20_chars)

        # assertion
        self.assertEqual(
            "Username must be between 4 and 20 chars", str(context.exception)
        )

    def test_it_creates_a_user_if_username_is_alpha_numeric(self):
        # set up
        actual_username_alpha_numeric = "random1"

        # execution
        new_user = UserFactory.make(actual_username_alpha_numeric)

        # assertion
        self.assertEqual(actual_username_alpha_numeric, new_user.username)

    def test_it_raises_exception_if_username_is_prohibited_word(self):
        # set up
        actual_prohibited_username_list = [
            "admin",
            "password",
            "superuser",
            "guest",
        ]
        actual_prohibited_username_choice = random.choice(
            actual_prohibited_username_list
        )

        # execution
        with self.assertRaises(InvalidUsername) as context:
            UserFactory.make(actual_prohibited_username_choice)

        # assertion
        self.assertEqual(
            "Username must not contain prohibited words like admin, etc.",
            str(context.exception),
        )

    def test_it_raises_exception_if_username_is_not_alpha_numeric(self):
        # set up
        actual_non_alpha_numeric_username = "random@%"

        # execution
        with self.assertRaises(InvalidUsername) as context:
            UserFactory.make(actual_non_alpha_numeric_username)

        # assertion
        self.assertEqual("Username must be alpha numeric!", str(context.exception))


if __name__ == "__main__":
    unittest.main()
