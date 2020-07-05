import time

from prometheus_client import Gauge
from prometheus_client import start_http_server

gauge_rate_luna_krw = Gauge("rate_luna_krw", "Rate for luna/krw")


def entrypoint() -> None:
    gauge_rate_luna_krw.set(10.2)
    start_http_server(8000)
    while True:
        time.sleep(10)
