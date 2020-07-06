import logging

from poche import Cache

from terra_price_exporter import helpers

from terra_price_exporter.exchange import exchanges

log = logging.getLogger(__name__)


class Pair:
    def __init__(
        self, ttl: int, exchange_name: str, currency: str, market: str
    ) -> None:
        self._cache = Cache(default_ttl=ttl)
        self.exchange = exchanges[exchange_name]()
        self.currency = currency
        self.market = market
        log.debug(f"new pair {self}")

    def __repr__(self) -> str:
        return (
            f"Pair({self._cache.default_ttl}, {self.exchange.name}, "
            f"{self.currency}, {self.market})"
        )

    def get_close(self) -> helpers.PROM_FLOAT:
        close = helpers.NOT_A_NUMBER
        try:
            close = self._cache.get("close")
        except KeyError:
            pass
        log.debug(f"pair {self} got queried for close {close}")
        return close

    def fetch_close(self) -> None:
        close = self.exchange.get(currency=self.currency, market=self.market,)
        self._cache.set("close", close)
        log.info(f"fetched {self} close for {close}")
