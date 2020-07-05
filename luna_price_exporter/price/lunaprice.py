import logging

from prometheus_client.metrics import MetricWrapperBase
import poche

from luna_price_exporter import helpers

log = logging.getLogger(__name__)


class LunaPrice:
    def __init__(self, ttl: int, metric: MetricWrapperBase) -> None:
        self._cache = poche.Cache(ttl)
        self._metric = metric
        self._metric.set_function(self.get)

    def get(self) -> helpers.PROM_FLOAT:
        price = helpers.NOT_A_NUMBER
        try:
            price = self._cache.get("price")
            log.debug(f"retrieved price {price} from cache for {self._metric}")
        except KeyError:
            log.debug(f"price is not yet fetched for {self._metric}")
        return price

    def fetch(self) -> None:
        raise NotImplementedError
