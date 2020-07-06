from typing import Dict
from typing import Optional
import json
import logging

import requests

from terra_price_exporter import helpers

log = logging.getLogger(__name__)


class BaseExchange:
    def __init__(
        self,
        name: str,
        url_template: str,
        uppercase_tickers: bool,
        currency_ticker_override: Dict[str, str] = {},
        market_ticker_override: Dict[str, str] = {},
        request_timeout: int = 1,
    ) -> None:
        self.name = name.lower()
        self.url_template = url_template
        self.uppercase_tickers = uppercase_tickers
        self.currency_ticker_override = currency_ticker_override
        self.market_ticker_override = market_ticker_override
        self.request_timeout = request_timeout

    def __str__(self):
        return self.name

    def _get(self, currency: str, market: Optional[str]) -> dict:
        try:
            if market:
                url = self.url_template.format(currency, market)
            else:
                url = self.url_template.format(currency)
            res = requests.get(url, timeout=self.request_timeout,)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException:
            log.error(f"could not GET from {res.url}")
        except json.decoder.JSONDecodeError:
            log.error(f"response parse json from {res.url}")
        return {}

    def _currency_ticker(self, currency: str) -> str:
        return (
            self.currency_ticker_override.get(currency, currency).upper()
            if self.uppercase_tickers
            else self.currency_ticker_override.get(currency, currency).lower()
        )

    def _market_ticker(self, market: str) -> str:
        return (
            self.market_ticker_override.get(market, market).upper()
            if self.uppercase_tickers
            else self.market_ticker_override.get(market, market).lower()
        )

    def get(self, currency: str, market: str) -> helpers.PROM_FLOAT:
        raise NotImplementedError
