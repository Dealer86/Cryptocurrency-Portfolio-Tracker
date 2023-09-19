import unittest

from domain_logic.crypto.crypto import Crypto


class TestCrypto(unittest.TestCase):
    def setUp(self):
        # Creating a sample Crypto object for testing
        self.crypto_data = {
            "name": "Bitcoin",
            "symbol": "BTC",
            "price": 45000.0,
            "last_updated": "2023-09-19",
            "units": 2.0,
        }
        # **self.crypto_data is the syntax for dictionary unpacking in Python.
        # It takes all the key-value pairs from self.crypto_data and passes them
        # as keyword arguments to the Crypto class constructor.
        self.crypto = Crypto(**self.crypto_data)

    def test_initialization(self):
        self.assertEqual(self.crypto.name, "Bitcoin")
        self.assertEqual(self.crypto.symbol, "BTC")
        self.assertEqual(self.crypto.price, 45000.0)
        self.assertEqual(self.crypto.last_updated, "2023-09-19")
        self.assertEqual(self.crypto.units, 2.0)

    def test_from_dict(self):
        crypto_dict = {
            "name": "Ethereum",
            "symbol": "ETH",
            "price": 3500.0,
            "last_updated": "2023-09-18",
            "units": 5.0,
        }
        crypto_obj = Crypto.from_dict(crypto_dict)

        self.assertEqual(crypto_obj.name, "Ethereum")
        self.assertEqual(crypto_obj.symbol, "ETH")
        self.assertEqual(crypto_obj.price, 3500.0)
        self.assertEqual(crypto_obj.last_updated, "2023-09-18")
        self.assertEqual(crypto_obj.units, 5.0)

    def test_to_dict(self):
        crypto_dict = self.crypto.to_dict()

        self.assertEqual(crypto_dict["name"], "Bitcoin")
        self.assertEqual(crypto_dict["symbol"], "BTC")
        self.assertEqual(crypto_dict["price"], 45000.0)
        self.assertEqual(crypto_dict["last_updated"], "2023-09-19")
        self.assertEqual(crypto_dict["units"], 2.0)


if __name__ == "__main__":
    unittest.main()
