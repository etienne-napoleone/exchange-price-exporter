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
        self.queue: queue.Queue = queue.Queue()
        self.interval = interval
        self.threads = []
        for _ in range(threads):
            thread = threading.Thread(target=self.worker)
            thread.setDaemon(True)
            self.threads.append(thread)
        self.metrics = dict(
            candle=Gauge(
                name="candle",
                documentation="Exchange candle for a currency on a market",
                labelnames=["exchange", "currency", "market", "olhcv"],
            )
        )
        self.pairs = [
            Pair(
                ttl=self.interval * 60 * 2,
                exchange_name=pair.exchange,
                currency=pair.currency,
                market=pair.market,
                gauge=self.metrics["candle"],
            )
            for pair in pairs
        ]
        log.debug(f"created metrics {self.metrics}")

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
