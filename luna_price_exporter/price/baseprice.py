from typing import List
import logging

from prometheus_client import Gauge

# from prometheus_client.metrics import MetricWrapperBase
import poche

from luna_price_exporter.exchange.baseexchange import BaseExchange
from luna_price_exporter.pair import Pair

log = logging.getLogger(__name__)


class BasePrice:
    def __init__(
        self, ttl: int, market: str, exchanges: List[BaseExchange]
    ) -> None:
        self._cache = poche.Cache(ttl)
        self.market = market
        self.metric = Gauge(
            name=f"luna_price_u{self.market}",
            documentation=f"Price of luna on the {self.market} maket",
            labelnames=["exchange"],
        )
        log.debug(f"new metric {self.metric}")
        self.pairs = {}
        for exchange in exchanges:
            pair = Pair(
                ttl=ttl,
                exchange=exchange,
                currency="luna",
                market=self.market,
            )
            self.pairs[exchange.name] = pair
            self.metric.labels(exchange=exchange.name).set_function(
                self.pairs[exchange.name].get
            )
            log.debug(f"new pair for market {self.market} on {exchange}")

    def fetch(self) -> None:
        raise NotImplementedError
