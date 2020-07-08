from exchange_price_exporter import helpers


class Candle:
    def __init__(
        self,
        open: helpers.PROM_FLOAT,
        low: helpers.PROM_FLOAT,
        high: helpers.PROM_FLOAT,
        close: helpers.PROM_FLOAT,
        volume: helpers.PROM_FLOAT,
    ) -> None:
        olhcv = dict(open=open, low=low, high=high, close=close, volume=volume)
        for key, item in olhcv.items():
            try:
                setattr(self, key, float(item))
            except (ValueError, TypeError):
                setattr(self, key, helpers.NOT_A_NUMBER)

    def __repr__(self) -> str:
        return "Candle({}, {}, {}, {}, {})".format(
            self.open, self.low, self.high, self.close, self.volume
        )
