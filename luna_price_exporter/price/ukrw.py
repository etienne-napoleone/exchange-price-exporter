import logging

from prometheus_client import Gauge
import requests

from luna_price_exporter import helpers
from luna_price_exporter.price.lunaprice import LunaPrice

log = logging.getLogger(__name__)


class Ukrw(LunaPrice):
    def __init__(self, ttl: int) -> None:
        LunaPrice.__init__(
            self,
            ttl=ttl,
            metric=Gauge("luna_price_ukrw", "Luna price in ukrw"),
        )
        log.info(f"new metric {self._metric}")

    def fetch(self) -> None:
        price: helpers.PROM_FLOAT = helpers.NOT_A_NUMBER
        try:
            res = requests.get(
                "https://api.coinone.co.kr/ticker/?currency=LUNA", timeout=1
            )
            res.raise_for_status()
            last = res.json().get("last")
            if last:
                price = float(last) * helpers.MICRO
                log.info(f"fetched price {price} for {self._metric}")
        except requests.exceptions.RequestException as e:
            log.warning(f"could not fetch price for {self._metric}, {e}")
        except ValueError as e:
            log.warning(
                f"fetched price for {self._metric} was not a valid value, {e}"
            )
        self._cache.set("price", price)
