import toml


class Config:
    def __init__(self, path: str) -> None:
        with open(path) as f:
            self._raw_config = toml.load(f)
        self.server = ServerConfig(data=self._raw_config.get("server", {}))
        self.log = LogConfig(data=self._raw_config.get("log", {}))
        self.exporter = ExporterConfig(
            data=self._raw_config.get("exporter", {})
        )


class ServerConfig:
    def __init__(self, data: dict) -> None:
        self.port = int(data.get("port", 8000))


class LogConfig:
    def __init__(self, data: dict) -> None:
        self.debug = bool(data.get("debug", False))


class ExporterConfig:
    def __init__(self, data: dict) -> None:
        self.interval = int(data.get("interval", 10))
        self.pairs = [
            ExporterPairConfig(pair) for pair in list(data.get("pairs", {}))
        ]


class ExporterPairConfig:
    def __init__(self, data: dict) -> None:
        self.exchange = str(data["exchange"])
        self.currency = str(data["currency"])
        self.market = str(data["market"])
