from typing import List
import logging

import time

from prometheus_client import Gauge

from exchange_price_exporter.config import ExporterPairConfig
from exchange_price_exporter.pair import Pair

log = logging.getLogger(__name__)


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
                ttl=self.interval * 2,
                exchange_name=pair.exchange,
                currency=pair.currency,
                market=pair.market,
                gauge=self.metrics["candle"],
            )
            for pair in pairs
        ]

    def start(self) -> None:
        while True:
            for pair in self.pairs:
                log.debug(f"fetching candle for pair {pair}")
                pair.get()
            log.debug(f"sleeping {self.interval}")
            time.sleep(self.interval)
