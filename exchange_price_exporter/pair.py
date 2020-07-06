from typing import Callable
import logging

from poche import Cache

from exchange_price_exporter import helpers
from exchange_price_exporter import exchanges

log = logging.getLogger(__name__)


class Pair:
    def __init__(
        self, ttl: int, exchange_name: str, currency: str, market: str
    ) -> None:
        self._cache = Cache(default_ttl=ttl)
        self.exchange = exchanges.get_by_name(exchange_name)()
        self.currency = currency
        self.market = market
        log.debug(f"new pair {self}")

    def __repr__(self) -> str:
        return (
            f"Pair({self._cache.default_ttl}, {self.exchange.name}, "
            f"{self.currency}, {self.market})"
        )

    def get_open(self) -> helpers.PROM_FLOAT:
        res = helpers.NOT_A_NUMBER
        try:
            res = self._cache.get("open")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for open {res}")
        return res

    def get_low(self) -> helpers.PROM_FLOAT:
        res = helpers.NOT_A_NUMBER
        try:
            res = self._cache.get("low")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for low {res}")
        return res

    def get_high(self) -> helpers.PROM_FLOAT:
        res = helpers.NOT_A_NUMBER
        try:
            res = self._cache.get("high")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for high {res}")
        return res

    def get_close(self) -> helpers.PROM_FLOAT:
        res = helpers.NOT_A_NUMBER
        try:
            res = self._cache.get("close")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for close {res}")
        return res

    def get_volume(self) -> helpers.PROM_FLOAT:
        res = helpers.NOT_A_NUMBER
        try:
            res = self._cache.get("volume")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for volume {res}")
        return res

    def get_function(self, olhcv: str) -> Callable[[], helpers.PROM_FLOAT]:
        functions = dict(
            open=self.get_open,
            low=self.get_low,
            high=self.get_high,
            close=self.get_close,
            volume=self.get_volume,
        )
        return functions[olhcv]

    def fetch(self, olhcv: str) -> None:
        res = self.exchange.get(
            currency=self.currency, market=self.market, olhcv=olhcv
        )
        self._cache.set(olhcv, res)
        log.info(f"fetched {self} {olhcv} for {res}")
