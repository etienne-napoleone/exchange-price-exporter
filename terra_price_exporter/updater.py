from typing import List
import logging

import time

from prometheus_client import Gauge

from terra_price_exporter.config import ExporterPairConfig
from terra_price_exporter.pair import Pair

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
                ttl=self.interval + 2,
                exchange_name=pair.exchange,
                currency=pair.currency,
                market=pair.market,
            )
            for pair in pairs
        ]
        for pair in self.pairs:
            self.metrics["candle"].labels(
                exchange=pair.exchange.name,
                currency=pair.currency,
                market=pair.market,
                olhcv="close",
            ).set_function(pair.get_close)
            log.debug(f"binded metrics to pair {pair}")

    def start(self) -> None:
        while True:
            for pair in self.pairs:
                log.debug(f"fetching pair {pair}")
                pair.fetch_close()
            log.debug(f"sleeping {self.interval}")
            time.sleep(self.interval)
