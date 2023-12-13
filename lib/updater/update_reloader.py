import os
import sys
import time
from threading import Thread
from typing import Callable

from lib import melman_logging
from lib.melman_config import CHECK_FOR_UPDATES_INTERVAL
from lib.updater.melman_updater import MelmanUpdater

logger = melman_logging.get_logger("MelmanAutoUpdater")


class Interval:
    func: Callable[..., object]
    interval: float

    def __init__(self, interval: float, function: Callable[..., object]):
        self.func = function
        self.interval = interval

    def start(self) -> None:
        Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while True:
            time.sleep(self.interval)
            self.func()


class UpdateReloader:
    git_repo: str

    def __init__(self, git_repo: str) -> None:
        self.git_repo = git_repo

    def start_async(self) -> None:
        """
        Starts the update reloader in a new thread.
        """
        logger.info("Starting update reloader")
        Interval(CHECK_FOR_UPDATES_INTERVAL, self._updater_thread).start()

    def _updater_thread(self) -> None:
        updater = MelmanUpdater(self.git_repo)

        if updater.update():
            self._restart()

    @staticmethod
    def _restart() -> None:
        logger.info("Executing restart for entire Melman process")
        exit(os.system(" ".join(sys.argv)))
