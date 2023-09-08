import requests
import logging
from domain_logic.crypto.crypto import Crypto
from exceptions.exceptions import InvalidCoinId


class CryptoFactory:
    @classmethod
    def make(cls, coins_id: str) -> Crypto:
        base_url = "https://api.coingecko.com/api/v3"
        endpoint = f"/coins/{coins_id}"
        try:
            logging.info(
                "CryptoFactory executing make command, making a get request to Coingecko url..."
            )
            response = requests.get(base_url + endpoint)
            if response.status_code == 200:
                logging.info("CryptoFactory successfully executed the get request.")
                data = response.json()
                if data is not None:
                    logging.info(
                        f"CryptoFactory successfully created a Crypto object for coin with ticker {coins_id}."
                    )
                    return Crypto(
                        name=data["name"],
                        price=data["market_data"]["current_price"]["usd"],
                        last_updated=data["last_updated"],
                        symbol=data["symbol"],
                        units=0,
                    )
                else:
                    logging.warning(
                        f"CryptoFactory could not retrieve data for {coins_id}. Data is None"
                    )
                    raise InvalidCoinId(f"Could not retrieve data for {coins_id}!")
            elif response.status_code == 404:
                logging.warning(
                    f"CryptoFactory could not retrieve data for {coins_id},"
                    f"it doesn't exist! Try another coin id/ticker."
                )
                raise InvalidCoinId(f"Coin {coins_id} does not exist! Try another one.")
        except Exception as e:
            raise InvalidCoinId(str(e))
