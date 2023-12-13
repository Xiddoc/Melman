"""
The root handler for the Bot, which passes the rest of the logic onto other components.
"""

from telegram.ext import ApplicationBuilder, Defaults

from lib.resolver.melman_types import MelmanApp
from lib.updater.update_reloader import UpdateReloader
from modules import MELMAN_MODULES


class MelmanCore:

    def __init__(self, api_token: str, update_git_repo_url: str) -> None:
        self._api_key = api_token
        self.git_repo = update_git_repo_url

    def start(self) -> None:
        self._start_auto_updater()
        self._start_telegram_application()

    def _start_auto_updater(self) -> None:
        reloader = UpdateReloader(self.git_repo)
        reloader.start_async()

    def _start_telegram_application(self) -> None:
        defaults = Defaults(block=False)
        application = ApplicationBuilder().token(self._api_key).defaults(defaults).build()
        self._register_modules(application)
        application.run_polling()

    @staticmethod
    def _register_modules(app: MelmanApp) -> None:
        for module in MELMAN_MODULES:
            module.register_module(app)
