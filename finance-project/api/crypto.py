from fastapi import APIRouter

from api.models.crypto_models import CryptoSchema
from api.cryptocurrency_price_history import CryptoCurrencyPriceHistory
from api.cryptocurrency_market_cap import CryptocurrencyMarketCap
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
    return CryptoCurrencyPriceHistory.get_cryptocurrency_price_history(
        coin_id, start_date, end_date
    )


@crypto_router.get("{coin_id}/market_cap")
def get_historical_market_cap(coin_id: str, currency: str = "usd", days: int = 7):
    return CryptocurrencyMarketCap.get_historical_market_cap(coin_id, currency, days)
