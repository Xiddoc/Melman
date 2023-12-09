"""
The root handler for the Bot, which passes the rest of the logic onto other components.
"""

from telegram.ext import ApplicationBuilder, Application

from lib.melman_banner import MELMAN_BANNER
from modules import MELMAN_MODULES


class MelmanCore:

    def __init__(self, api_token: str) -> None:
        self._api_key = api_token

    def start(self) -> None:
        print(MELMAN_BANNER)
        self._start_telegram_application()

    def _start_telegram_application(self) -> None:
        application = ApplicationBuilder().token(self._api_key).build()
        self._register_modules(application)
        application.run_polling()

    @staticmethod
    def _register_modules(app: Application) -> None:
        for module in MELMAN_MODULES:
            module.register_module(app)
