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

    def get(
        self, currency: str, market: str, olhcv: str
    ) -> helpers.PROM_FLOAT:
        params = dict(
            currency=self._currency_ticker(currency),
            market=self._market_ticker(market),
        )
        data = self._get(**params).get("data", {})
        if olhcv == "open":
            res = data.get("opening_price")
        elif olhcv == "low":
            res = data.get("min_price")
        elif olhcv == "high":
            res = data.get("max_price")
        elif olhcv == "close":
            res = data.get("closing_price")
        elif olhcv == "volume":
            res = data.get("units_traded")
        if res:
            try:
                return float(res)
            except ValueError:
                pass
        return helpers.NOT_A_NUMBER
