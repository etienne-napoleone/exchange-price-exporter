import logging

__version__ = "0.2.0"

logging.basicConfig(
    format="%(asctime)s - %(thread)d:%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("schedule").setLevel(logging.ERROR)
