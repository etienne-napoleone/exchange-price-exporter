from prometheus_client import start_http_server

from luna_price_exporter.config import Config
from luna_price_exporter.updater import Updater


def entrypoint() -> None:
    config = Config()
    updater = Updater(interval=config.interval, denoms=config.denoms)
    start_http_server(port=config.port)
    updater.start()
