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
            url_template=(
                "https://tb.coinone.co.kr/api/v1/chart/olhc"
                "/?site=coinone{}&type=1m"
            ),
            uppercase_tickers=True,
        )

    def get(self, currency: str, market: str) -> Candle:
        if market != "krw":
            log.warning("coinone only supports the krw market")
            return Candle(
                **helpers.EMPTY_CANDLE
            )  # coinone only support the krw market
        data = self._get(
            currency=self._currency_ticker(currency)
            if currency != "btc"
            else "",
            market=self._currency_ticker(market),
        ).get("data")
        if data:
            data_element = data.pop()
            return Candle(
                open=data_element.get("Open"),
                low=data_element.get("Low"),
                high=data_element.get("High"),
                close=data_element.get("Close"),
                volume=data_element.get("Volume"),
            )
        else:
            return Candle(**helpers.EMPTY_CANDLE)
