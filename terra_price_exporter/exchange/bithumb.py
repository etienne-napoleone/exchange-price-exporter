import logging

from terra_price_exporter import helpers
from terra_price_exporter.exchange.baseexchange import BaseExchange

log = logging.getLogger(__name__)


class Bithumb(BaseExchange):
    def __init__(self) -> None:
        BaseExchange.__init__(
            self,
            name="bithumb",
            url_template="https://api.bithumb.com/public/ticker/{}_{}",
            uppercase_tickers=True,
        )

    def get(self, currency: str, market: str) -> helpers.PROM_FLOAT:
        price = (
            self._get(
                currency=self.currency_ticker(currency),
                market=self.market_ticker(market),
            )
            .get("data", {})
            .get("closing_price")
        )
        if price:
            try:
                return float(price) * helpers.MICRO
            except ValueError:
                pass
        return helpers.NOT_A_NUMBER
