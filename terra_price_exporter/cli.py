import logging

from prometheus_client import start_http_server
import click

from terra_price_exporter import __version__
from terra_price_exporter.config import Config
from terra_price_exporter.updater import Updater

log = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c",
    default="./config.toml",
    type=click.Path(exists=True, dir_okay=False),
    help="Toml config file",
)
@click.version_option(version=__version__, message="%(prog)s, v%(version)s")
def entrypoint(c: str) -> None:
    config = Config(c)
    if config.log.debug:
        logging.getLogger("terra_price_exporter").setLevel(logging.DEBUG)
        logging.getLogger("terra_price_exporter").warning("debug logs enabled")
    updater = Updater(
        interval=config.exporter.interval, pairs=config.exporter.pairs
    )
    start_http_server(port=config.server.port)
    log.info(f"starting terra_price_exporter v{__version__}")
    updater.start()
