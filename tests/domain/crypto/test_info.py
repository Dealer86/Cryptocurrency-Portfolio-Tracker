import unittest
from unittest.mock import Mock, patch
from domain_logic.crypto.crypto_info import CryptoInfo


class TestCryptoInfo(unittest.TestCase):
    def test_get_historical_market_cap(self):
        # Mock the requests.get function
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "market_caps": [(1629194400000, 1000000000), (1629280800000, 1100000000)]
        }

        with patch("requests.get", return_value=mock_response):
            result = CryptoInfo.get_historical_market_cap("bitcoin", "usd", 7)

        self.assertTrue(result)

    def test_get_cryptocurrency_price_history(self):
        # Mock the requests.get function
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "prices": [(1629194400000, 50000), (1629280800000, 55000)]
        }

        with patch("requests.get", return_value=mock_response):
            result = CryptoInfo.get_cryptocurrency_price_history(
                "bitcoin", "2023-01-01", "2023-01-02"
            )

        self.assertTrue(result)
        self.assertEqual(result.media_type, "image/png")

    def test_invalid_date_format(self):
        result = CryptoInfo.get_cryptocurrency_price_history(
            "bitcoin", "2023-01-01", "invalid_date"
        )

        self.assertEqual(result, "error invalid date format!")

    @classmethod
    def tearDownClass(cls) -> None:
        import os

        files = os.listdir(".")
        graphs = [f for f in files if f.endswith(".png")]
        for g in graphs:
            os.remove(g)


if __name__ == "__main__":
    unittest.main()
