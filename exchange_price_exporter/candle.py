from typing import Any

from exchange_price_exporter import helpers


class Candle:
    def __init__(
        self, open: Any, low: Any, high: Any, close: Any, volume: Any,
    ) -> None:
        self.open = helpers.NOT_A_NUMBER
        self.low = helpers.NOT_A_NUMBER
        self.high = helpers.NOT_A_NUMBER
        self.close = helpers.NOT_A_NUMBER
        self.volume = helpers.NOT_A_NUMBER
        for key, item in dict(
            open=open, low=low, high=high, close=close, volume=volume
        ).items():
            try:
                setattr(self, key, float(item))
            except (ValueError, TypeError):
                pass

    def __repr__(self) -> str:
        return "Candle({}, {}, {}, {}, {})".format(
            self.open, self.low, self.high, self.close, self.volume
        )
