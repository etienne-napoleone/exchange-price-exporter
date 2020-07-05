from prometheus_client import Gauge
import requests

from luna_price_exporter import helpers
from luna_price_exporter.price.lunaprice import LunaPrice


class Ukrw(LunaPrice):
    def __init__(self, ttl: int) -> None:
        LunaPrice.__init__(
            self,
            ttl=ttl,
            metric=Gauge("luna_price_ukrw", "Luna price in ukrw"),
        )

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
        except requests.exceptions.RequestException:
            pass
        except ValueError:
            pass
        self._cache.set("price", price)
