import logging

# from prometheus_client import Gauge
# import requests

# from terra_price_exporter import helpers
from terra_price_exporter.price.baseprice import BasePrice
from terra_price_exporter.exchange import Coinone
from terra_price_exporter.exchange import Bithumb

log = logging.getLogger(__name__)


class Ukrw(BasePrice):
    def __init__(self, ttl: int) -> None:
        BasePrice.__init__(
            self, market="krw", ttl=ttl, exchanges=[Coinone(), Bithumb()]
        )

    def fetch(self) -> None:
        for pair in self.pairs.values():
            pair.set()
