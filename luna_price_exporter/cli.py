import logging

from prometheus_client import start_http_server

from luna_price_exporter import __version__
from luna_price_exporter.config import Config
from luna_price_exporter.updater import Updater

log = logging.getLogger(__name__)


def entrypoint() -> None:
    config = Config()
    if config.debug:
        logging.getLogger("luna_price_exporter").setLevel(logging.DEBUG)
        logging.getLogger("luna_price_exporter").warning("debug logs enabled")
    log.debug(f"loaded config {config.__dict__}")
    updater = Updater(interval=config.interval, denoms=config.denoms)
    start_http_server(port=config.port)
    log.info(f"starting luna_price_exporter v{__version__}")
    updater.start()
