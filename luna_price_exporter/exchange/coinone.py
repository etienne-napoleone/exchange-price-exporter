import logging

from luna_price_exporter import helpers
from luna_price_exporter.exchange.baseexchange import BaseExchange

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
        if market != "krw":
            return helpers.NOT_A_NUMBER  # coinone only support the krw market
        price = self._get(
            currency=self.currency_ticker(currency), market=None
        ).get("last")
        if price:
            try:
                return float(price) * helpers.MICRO
            except ValueError:
                pass
        return helpers.NOT_A_NUMBER
