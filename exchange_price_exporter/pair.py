import logging

from prometheus_client import Gauge
from poche import Cache

from exchange_price_exporter import helpers
from exchange_price_exporter import exchanges


log = logging.getLogger(__name__)


class Pair:
    def __init__(
        self,
        ttl: int,
        exchange_name: str,
        currency: str,
        market: str,
        gauge: Gauge,
    ) -> None:
        self.cache = Cache(default_ttl=ttl)
        self.gauge = gauge
        self.exchange = exchanges.get_by_name(exchange_name)()
        self.currency = currency
        self.market = market
        log.debug(f"new pair {self}")

    def __repr__(self) -> str:
        return (
            f"Pair({self.cache.default_ttl}, {self.exchange.name}, "
            f"{self.currency}, {self.market})"
        )

    def get(self) -> None:
        try:
            candle = self.cache.get("candle")
        except KeyError:
            candle = self.exchange.get(
                currency=self.currency, market=self.market
            )
            self.cache.set("candle", candle)
        for olhcv in helpers.EMPTY_CANDLE.keys():
            self.gauge.labels(
                exchange=self.exchange.name,
                currency=self.currency,
                market=self.market,
                olhcv=olhcv,
            ).set(candle.__dict__[olhcv])
        log.info(f"fetched {candle} for {self}")
