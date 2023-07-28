import uuid
import requests
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from fastapi import APIRouter
from fastapi.responses import FileResponse

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
                if data:
                    try:
                        return Crypto(
                            name=data["name"],
                            price=data["market_data"]["current_price"]["usd"],
                            last_updated=data["last_updated"],
                            symbol=data["symbol"],
                        )
                    except AttributeError as e:
                        raise InvalidCoinId("Coin Id does not exist! Error: " + str(e))

        except Exception as e:
            raise InvalidCoinId("Coin Id does not exist!")
