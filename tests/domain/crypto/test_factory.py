import unittest
from unittest import mock
from unittest.mock import patch

from domain_logic.crypto.crypto_factory import CryptoFactory
from exceptions.exceptions import InvalidCoinId


class TestCryptoFactory(unittest.TestCase):
    @patch("domain_logic.crypto.crypto_factory.requests.get")
    def test_make_valid_coin(self, mock_requests_get):
        # Mock the response for a valid coin
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Bitcoin",
            "market_data": {
                "current_price": {"usd": 50000},
            },
            "last_updated": "2023-09-19T10:30:0001111",
            "symbol": "BTC",
        }
        mock_requests_get.return_value = mock_response

        crypto = CryptoFactory.make("bitcoin")
        self.assertEqual(crypto.name, "Bitcoin")
        self.assertEqual(crypto.price, 50000)
        self.assertEqual(crypto.last_updated, "2023-09-19T10:30:00")
        self.assertEqual(crypto.symbol, "BTC")
        self.assertEqual(crypto.units, 0)

    @patch("domain_logic.crypto.crypto_factory.requests.get")
    def test_make_invalid_coin(self, mock_requests_get):
        # Mock the response for an invalid coin
        mock_response = {"status_code": 404}
        mock_requests_get.return_value = mock_response

        with self.assertRaises(InvalidCoinId):
            CryptoFactory.make("invalidcoin")


if __name__ == "__main__":
    unittest.main()
