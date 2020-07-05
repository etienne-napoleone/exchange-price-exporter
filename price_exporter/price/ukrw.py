from typing import Union

from prometheus_client import Gauge
import poche
import requests

from price_exporter import helpers


class Ukrw:
    def __init__(self, ttl: int = 30) -> None:
        self._cache = poche.Cache(ttl)
        self._metric = Gauge("price_ukrw", "Price of luna in ukrw")
        self._metric.set_function(self.get)

    def get(self) -> Union[float, str]:
        price = helpers.NOT_A_NUMBER
        try:
            price = self._cache.get("price")
        except KeyError:
            pass
        return price

    def fetch(self) -> None:
        price = helpers.NOT_A_NUMBER
        try:
            res = requests.get(
                "https://api.coinone.co.kr/ticker/?currency=LUNA", timeout=1
            )
            res.raise_for_status()
            last = res.json().get("last")
            if last:
                price = float(last) / helpers.MICRO
        except requests.exceptions.RequestException:
            pass
        except ValueError:
            pass
        self._cache.set("price", price)
