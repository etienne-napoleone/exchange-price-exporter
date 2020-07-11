from exchange_price_exporter.exchanges.bithumb import Bithumb
from exchange_price_exporter.exchanges.coinone import Coinone
from exchange_price_exporter.exchanges.kucoin import Kucoin

integrations = dict(bithumb=Bithumb, coinone=Coinone, kucoin=Kucoin)
