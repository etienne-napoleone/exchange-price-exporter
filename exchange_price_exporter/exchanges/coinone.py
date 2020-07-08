import logging

from exchange_price_exporter import helpers
from exchange_price_exporter.candle import Candle
from exchange_price_exporter.exchanges.baseexchange import BaseExchange

log = logging.getLogger(__name__)


class Coinone(BaseExchange):
    def __init__(self) -> None:
        BaseExchange.__init__(
            self,
            name="coinone",
            url_template="https://api.coinone.co.kr/ticker/?currency={}",
            uppercase_tickers=True,
        )

    def get(self, currency: str, market: str) -> helpers.PROM_FLOAT:
        params = dict(
            currency=self._currency_ticker(currency),
            market=self._market_ticker(market),
        )
        if market != "krw":
            return helpers.NOT_A_NUMBER  # coinone only support the krw market
        data = self._get(**params)
        return Candle(
            open=data.get("first"),
            low=data.get("low"),
            high=data.get("high"),
            close=data.get("last"),
            volume=data.get("volume"),
        )
