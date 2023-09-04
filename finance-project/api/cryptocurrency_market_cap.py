import uuid
import requests
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse


class CryptocurrencyMarketCap:
    @classmethod
    def get_historical_market_cap(cls, coin_id: str, currency: str, days: int):
        base_url = "https://api.coingecko.com/api/v3"
        url = f"{base_url}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": currency,  # Currency in which prices are displayed (e.g., USD)
            "days": days,  # Number of days for historical data
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            market_caps = data.get("market_caps", [])
            # Extract timestamps and market caps
            timestamps_for_market_caps, market_caps_values = zip(*market_caps)
            # # Convert timestamps to datetime objects
            timestamps_for_market_caps = [
                datetime.fromtimestamp(ts / 1000) for ts in timestamps_for_market_caps
            ]
            # # Create a Matplotlib figure and plot the data
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps_for_market_caps, market_caps_values)
            plt.title(f"{coin_id.title()} Historical Market Caps Chart")
            plt.xlabel("Date")
            plt.ylabel(
                f"Market Cap(Current Price per Token × Total Circulating Supply)"
            )
            plt.grid(True)
            png_name = f"historical_market_cap_for_{coin_id}_{uuid.uuid4()}.png"
            plt.savefig(png_name)
            plt.clf()
            return FileResponse(png_name, media_type="image/png")
