from typing import List
import time

from price_exporter.price import prices


class Updater:
    def __init__(self, interval: int, denoms: List[str]) -> None:
        self.interval = interval
        self.denoms = denoms
        self.prices = {
            key: Price(interval + 2) for key, Price in prices.items()
        }

    def start(self) -> None:
        while True:
            for denom in self.denoms:
                if denom in prices.keys():
                    self.prices[denom].fetch()
            time.sleep(self.interval)
