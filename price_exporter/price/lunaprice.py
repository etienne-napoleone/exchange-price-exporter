from prometheus_client.metrics import MetricWrapperBase
import poche

from price_exporter import helpers


class LunaPrice:
    def __init__(self, ttl: int, metric: MetricWrapperBase) -> None:
        self._cache = poche.Cache(ttl)
        self._metric = metric
        self._metric.set_function(self.get)

    def get(self) -> helpers.PROM_FLOAT:
        price = helpers.NOT_A_NUMBER
        try:
            price = self._cache.get("price")
        except KeyError:
            pass
        return price

    def fetch(self) -> None:
        raise NotImplementedError
