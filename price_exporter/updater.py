from typing import List
import time

from price_exporter.price import prices


class Updater:
    def __init__(
        self, interval: int = 10, denoms: List[str] = ["ukrw"]
    ) -> None:
        self.interval = interval
        self.denoms = denoms

    def start(self) -> None:
        while True:
            for denom in self.denoms:
                if denom in prices.keys():
                    prices[denom].fetch()
            time.sleep(20)
