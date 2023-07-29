import sqlite3

from domain_logic.crypto.crypto import Crypto
from domain_logic.user.user import User


class CryptoRepo:
    # TODO refactor this code in the persistence layer and implement Repo so that it will manage Crypto objects
    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS crypto "
                "(user_id TEXT, name TEXT, symbol TEXT, price FLOAT, last_updated TEXT, units FLOAT)"
            )
            cursor.execute(
                "INSERT INTO crypto VALUES (?, ?, ?, ? ,?, ?)",
                (
                    user_id,
                    cryptocurrency.name,
                    cryptocurrency.symbol,
                    cryptocurrency.price,
                    cryptocurrency.last_updated,
                    cryptocurrency.units,
                ),
            )
            conn.commit()

    def get_crypto_for_user(self, user_id: str) -> list[Crypto]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crypto WHERE user_id = (?)", (user_id,))
            tuple_data = cursor.fetchall()
            print(tuple_data)
            return [
                Crypto(
                    name=c[1],
                    symbol=c[2],
                    price=c[3],
                    last_updated=c[4],
                    units=c[5],
                )
                for c in tuple_data
            ]
