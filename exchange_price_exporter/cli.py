import logging

from prometheus_client import start_http_server
import click

from exchange_price_exporter import __version__
from exchange_price_exporter.config import Config
from exchange_price_exporter.updater import Updater

log = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c",
    default="./config.toml",
    type=click.Path(exists=True, dir_okay=False),
    help="TOML config file.",
)
@click.version_option(version=__version__, message="%(prog)s, v%(version)s")
def entrypoint(c: str) -> None:
    """Exchange price exporter."""
    log.info(f"starting exchange_price_exporter v{__version__}")
    config = Config(c)
    if config.log.debug:
        logging.getLogger("exchange_price_exporter").setLevel(logging.DEBUG)
        logging.getLogger("exchange_price_exporter").warning(
            "debug logs enabled"
        )
    updater = Updater(
        interval=config.exporter.interval,
        start_at_second=config.exporter.start_at_second,
        pairs=config.exporter.pairs,
        threads=config.exporter.threads,
    )
    start_http_server(port=config.server.port)
    updater.start()
