import os


class Config:
    def __init__(self):
        self.debug = os.getenv("DEBUG")
        self.port = int(os.getenv("PORT", "8000"))
        self.interval = int(os.getenv("INTERVAL", "10"))
        self.denoms = (
            [denom.strip() for denom in os.getenv("DENOMS").split(",")]
            if os.getenv("DENOMS")
            else []
        )
