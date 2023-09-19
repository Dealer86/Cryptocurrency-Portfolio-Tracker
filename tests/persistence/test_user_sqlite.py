import sqlite3
import unittest
from domain_logic.user.user_factory import UserFactory
from persistence.user_persistence_sqlite import UserPersistenceSqlite


class UserPersistenceSqliteTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.user_persistence_sqlite = UserPersistenceSqlite("user_test.db")
        username = "random"
        self.new_user = UserFactory.make(username)

    def test_get_all_gets_empty_list_if_database_is_empty(self):
        # execution
        all_users = self.user_persistence_sqlite.get_all()

        # assertion
        self.assertEqual([], all_users)

    def test_it_adds_a_user(self):
        # execution
        self.user_persistence_sqlite.add(self.new_user)
        actual_new_user = [u.username for u in self.user_persistence_sqlite.get_all()]

        # assertion
        self.assertIn(self.new_user.username, actual_new_user)

    def test_it_delete_a_user(self):
        # set up
        self.user_persistence_sqlite.add(self.new_user)

        # execution
        self.user_persistence_sqlite.delete(str(self.new_user.id))
        all_users = self.user_persistence_sqlite.get_all()

        # assertion
        self.assertNotIn(self.new_user.username, all_users)

    def test_it_updates_a_user(self):
        # set up
        self.user_persistence_sqlite.add(self.new_user)

        # execution
        actual_new_username = "newname"
        self.user_persistence_sqlite.update(str(self.new_user.id), actual_new_username)
        all_usernames = [u.username for u in self.user_persistence_sqlite.get_all()]

        # assertion
        self.assertIn(actual_new_username, all_usernames)

    @classmethod
    def tearDownClass(cls) -> None:
        with sqlite3.connect("user_test.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE users")


if __name__ == "__main__":
    unittest.main()
