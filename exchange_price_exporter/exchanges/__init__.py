from exchange_price_exporter.exchanges.bithumb import Bithumb
from exchange_price_exporter.exchanges.coinone import Coinone


def get_by_name(name: str):
    return dict(bithumb=Bithumb, coinone=Coinone)[name]
