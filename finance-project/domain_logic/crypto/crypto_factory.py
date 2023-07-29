import requests

from domain_logic.crypto.crypto import Crypto


class InvalidCoinId(Exception):
    pass


class CryptoFactory:
    @classmethod
    def make(cls, coins_id: str) -> Crypto:
        base_url = "https://api.coingecko.com/api/v3"
        endpoint = f"/coins/{coins_id}"
        try:
            response = requests.get(base_url + endpoint)
            if response.status_code == 200:
                data = response.json()
                if data is not None:  # Check if data is not None
                    return Crypto(
                        name=data["name"],
                        price=data["market_data"]["current_price"]["usd"],
                        last_updated=data["last_updated"],
                        symbol=data["symbol"],
                    )
                else:
                    raise InvalidCoinId(
                        "Coin Id does not exist. This is from Crypto obj return!"
                    )
            elif response.status_code == 404:
                raise InvalidCoinId("Coin Id does not exist!")

        except Exception as e:
            raise InvalidCoinId("Coin Id does not exist!")
