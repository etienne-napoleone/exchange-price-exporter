import logging
import signal

log = logging.getLogger(__name__)


class SignalHandler:
    stop = False
    signals = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM"}

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        log.debug("received {}, exiting...".format(self.signals[signum]))
        self.stop = True
