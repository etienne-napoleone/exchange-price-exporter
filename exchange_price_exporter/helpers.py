from typing import Union

NOT_A_NUMBER = "NaN"
MICRO = 0.000001
PROM_FLOAT = Union[str, float]
EMPTY_CANDLE = dict(
    open=NOT_A_NUMBER,
    low=NOT_A_NUMBER,
    high=NOT_A_NUMBER,
    close=NOT_A_NUMBER,
    volume=NOT_A_NUMBER,
)
