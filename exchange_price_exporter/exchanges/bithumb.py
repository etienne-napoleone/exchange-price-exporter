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
            url_template="https://api.bithumb.com/public/candlestick/{}_{}/1m",
            uppercase_tickers=True,
        )

    def get(self, currency: str, market: str) -> Candle:
        params = dict(
            currency=self._currency_ticker(currency),
            market=self._market_ticker(market),
        )
        data = self._get(**params).get("data")
        if data:
            data_element = data.pop()
            return Candle(
                open=data_element[1],
                low=data_element[4],
                high=data_element[3],
                close=data_element[2],
                volume=data_element[5],
            )
        else:
            return Candle(**helpers.EMPTY_CANDLE)
