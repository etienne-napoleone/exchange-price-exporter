import os


class Config:
    def __init__(self):
        self.port = int(os.getenv("PORT", "8000"))
        self.interval = int(os.getenv("INTERVAL", "10"))
        self.denoms = (
            os.getenv("DENOMS").split(",") if os.getenv("DENOMS") else []
        )