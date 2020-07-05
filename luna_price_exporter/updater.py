from typing import List
import logging
import time

from luna_price_exporter.price import prices

log = logging.getLogger(__name__)


class Updater:
    def __init__(self, interval: int, denoms: List[str]) -> None:
        self.interval = interval
        self.denoms = denoms
        self.prices = {
            key: Price(interval + 2) for key, Price in prices.items()
        }
        log.debug(f"updater initialized {self.__dict__}")

    def start(self) -> None:
        while True:
            for denom in self.denoms:
                if denom in prices.keys():
                    log.debug(f"fetching denom {denom}")
                    self.prices[denom].fetch()
                else:
                    log.error(
                        f"denom {denom} is not available "
                        "in luna_price_exporter"
                    )
            log.debug(f"sleeping {self.interval}")
            time.sleep(self.interval)
