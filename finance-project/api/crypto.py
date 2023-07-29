import uuid
import requests
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from fastapi import APIRouter
from fastapi.responses import FileResponse

from api.crypto_models import CryptoSchema
from domain_logic.crypto.crypto_factory import CryptoFactory


crypto_router = APIRouter(prefix="/crypto")
crypto_factory = CryptoFactory()


@crypto_router.get("{coins_id}", response_model=CryptoSchema)
def get_cryptocurrency_data(coins_id: str):
    crypto = crypto_factory.make(coins_id)
    return crypto


@crypto_router.get("{coin_id}/history")
def get_cryptocurrency_price_history(
    coin_id: str, start_date: str = "2023-01-01", end_date: str = "2023-07-28"
):
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"/coins/{coin_id}/market_chart/range"
    try:
        start_timestamp = int(
            datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc).timestamp()
        )
        end_timestamp = int(
            datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc).timestamp()
        )
    except ValueError:
        return "error invalid date format!"
    params = {"vs_currency": "usd", "from": start_timestamp, "to": end_timestamp}

    try:
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            price_history_data = response.json()
            if price_history_data:
                timestamps, prices = zip(*price_history_data["prices"])
                dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

                plt.figure(figsize=(12, 6))
                plt.plot(dates, prices)
                plt.title(f"{coin_id.capitalize()} Price History")
                plt.xlabel("Date")
                plt.ylabel("Price (USD)")
                plt.grid(True)
                plt.tight_layout()
                plt.xticks(rotation=45)
                image_name = f"{coin_id}-{uuid.uuid4()}.png"
                plt.savefig(image_name)
                return FileResponse(image_name, media_type="image/png")
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
