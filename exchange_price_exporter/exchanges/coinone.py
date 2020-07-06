import logging

from exchange_price_exporter import helpers
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

    def get(
        self, currency: str, market: str, olhcv: str
    ) -> helpers.PROM_FLOAT:
        params = dict(
            currency=self._currency_ticker(currency),
            market=self._market_ticker(market),
        )
        if market != "krw":
            return helpers.NOT_A_NUMBER  # coinone only support the krw market
        data = self._get(**params)
        if olhcv == "open":
            res = data.get("first")
        elif olhcv == "low":
            res = data.get("low")
        elif olhcv == "high":
            res = data.get("high")
        elif olhcv == "close":
            res = data.get("last")
        elif olhcv == "volume":
            res = data.get("volume")
        if res:
            try:
                return float(res)
            except ValueError:
                pass
        return helpers.NOT_A_NUMBER
