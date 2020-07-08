import logging

from exchange_price_exporter import helpers
from exchange_price_exporter.candle import Candle
from exchange_price_exporter.exchanges.baseexchange import BaseExchange

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
        params = dict(
            currency=self._currency_ticker(currency),
            market=self._market_ticker(market),
        )
        data = self._get(**params).get("data", {})
        return Candle(
            open=data.get("opening_price"),
            low=data.get("min_price"),
            high=data.get("max_price"),
            close=data.get("closing_price"),
            volume=data.get("units_traded"),
        )
