import sqlite3

from domain_logic.crypto.crypto import Crypto
from domain_logic.crypto.crypto_persistence_interface import CryptoPersistenceInterface


class CryptoSqlite(CryptoPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def add_crypto_to_user(self, user_id: str, cryptocurrency: Crypto):
        with sqlite3.connect(self.__file_path) as conn:
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
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM crypto WHERE user_id = (?)", (user_id,))
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
            list_of_tuple_data = cursor.fetchall()
            return [
                Crypto(
                    name=c[1],
                    symbol=c[2],
                    price=c[3],
                    last_updated=c[4],
                    units=c[5],
                )
                for c in list_of_tuple_data
            ]

    def calculate_total_crypto_value(self, user_id: str) -> float:
        with sqlite3.connect(self.__file_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "SELECT price FROM crypto WHERE user_id = (?)", (user_id,)
                )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return 0
            data = cursor.fetchall()
            # print(data)
            result = 0
            for every_price in data:
                number = every_price[0]
                result += number
            return result
