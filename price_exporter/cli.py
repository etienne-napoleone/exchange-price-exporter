from prometheus_client import start_http_server

from price_exporter.updater import Updater


def entrypoint() -> None:
    updater = Updater()
    start_http_server(8000)
    updater.start()
