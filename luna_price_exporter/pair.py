import logging

from poche import Cache

from luna_price_exporter import helpers
from luna_price_exporter.exchange.baseexchange import BaseExchange

log = logging.getLogger(__name__)


class Pair:
    def __init__(
        self, ttl: int, exchange: BaseExchange, currency: str, market: str
    ) -> None:
        self._cache = Cache(ttl)
        self.exchange = exchange
        self.currency = currency
        self.market = market

    def set(self) -> None:
        price = self.exchange.get(currency=self.currency, market=self.market)
        self._cache.set("price", price)
        log.info(
            f"set {self.currency}/{self.market} on {self.exchange} to {price}"
        )

    def get(self) -> helpers.PROM_FLOAT:
        price = helpers.NOT_A_NUMBER
        try:
            price = self._cache.get("price")
            log.debug(
                f"retrieved price {price} from cache for "
                f"{self.currency}/{self.market} on {self.exchange}"
            )
        except KeyError:
            log.debug(
                "price is not yet fetched for "
                f"{self.currency}/{self.market} on {self.exchange}"
            )
        return price
