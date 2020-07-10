from typing import List
import logging
import queue
import schedule
import threading
import time

from prometheus_client import Gauge

from exchange_price_exporter.config import ExporterPairConfig
from exchange_price_exporter.pair import Pair
from exchange_price_exporter.signalhandler import SignalHandler

log = logging.getLogger(__name__)


class Updater:
    def __init__(
        self,
        interval: int,
        start_at_second: int,
        pairs: List[ExporterPairConfig],
        threads: int,
    ) -> None:
        self.queue = queue.Queue()
        self.interval = interval
        self.threads = self.get_threads(threads)
        self.metrics = dict(
            candle=Gauge(
                name="candle",
                documentation="Exchange candle for a currency on a market",
                labelnames=["exchange", "currency", "market", "olhcv"],
            )
        )
        self.pairs = self.get_pairs(pairs)

        log.debug(f"created metrics {self.metrics}")

    def get_pairs(self, pairs: List[ExporterPairConfig]) -> List[Pair]:
        valid_pairs = []
        for pair in pairs:
            try:
                valid_pairs.append(
                    Pair(
                        ttl=self.interval * 60 * 2,
                        exchange_name=pair.exchange,
                        currency=pair.currency,
                        market=pair.market,
                        gauge=self.metrics["candle"],
                    )
                )
            except KeyError:
                log.warning(
                    f"ignored pair with unsuported exchange '{pair.exchange}'"
                )
        return valid_pairs

    def get_threads(self, count: int) -> List[threading.Thread]:
        threads = []
        for _ in range(count):
            thread = threading.Thread(target=self.worker)
            thread.setDaemon(True)
            threads.append(thread)
        return threads

    def worker(self) -> None:
        while 1:
            log.debug("worker waiting for a job")
            function = self.queue.get()
            log.debug("worker got a job")
            function()
            self.queue.task_done()
            log.debug("worker is done")

    def start(self) -> None:
        signal_handler = SignalHandler()
        for pair in self.pairs:
            log.debug(f"scheduling pair {pair}")
            schedule.every(self.interval).minutes.at(":30").do(
                self.queue.put, pair.get
            )
        for thread in self.threads:
            thread.start()
        while not signal_handler.stop:
            schedule.run_pending()
            time.sleep(1)
