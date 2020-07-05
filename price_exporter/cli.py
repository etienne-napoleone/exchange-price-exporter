from prometheus_client import start_http_server

from price_exporter.config import Config
from price_exporter.updater import Updater


def entrypoint() -> None:
    config = Config()
    updater = Updater(interval=config.interval, denoms=config.denoms)
    start_http_server(port=config.port)
    updater.start()
