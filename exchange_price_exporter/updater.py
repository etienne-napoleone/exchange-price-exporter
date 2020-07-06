from typing import List
import logging

import time

from prometheus_client import Gauge

from exchange_price_exporter.config import ExporterPairConfig
from exchange_price_exporter.pair import Pair

log = logging.getLogger(__name__)

OLHCV = ["open", "low", "high", "close", "volume"]


class Updater:
    def __init__(self, interval: int, pairs: List[ExporterPairConfig]) -> None:
        self.interval = interval
        self.metrics = dict(
            candle=Gauge(
                name="candle",
                documentation="Exchange candle for a currency on a market",
                labelnames=["exchange", "currency", "market", "olhcv"],
            )
        )
        log.debug(f"created metrics {self.metrics}")
        self.pairs = [
            Pair(
                ttl=self.interval + 2,
                exchange_name=pair.exchange,
                currency=pair.currency,
                market=pair.market,
            )
            for pair in pairs
        ]
        for pair in self.pairs:
            for olhcv in OLHCV:
                self.metrics["candle"].labels(
                    exchange=pair.exchange.name,
                    currency=pair.currency,
                    market=pair.market,
                    olhcv=olhcv,
                ).set_function(pair.get_function(olhcv))
                log.debug(f"binded metrics to pair {pair} - {olhcv}")

    def start(self) -> None:
        while True:
            for pair in self.pairs:
                for olhcv in OLHCV:
                    log.debug(f"fetching pair pair {pair} - {olhcv}")
                    pair.fetch(olhcv)
            log.debug(f"sleeping {self.interval}")
            time.sleep(self.interval)
