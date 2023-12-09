from typing import Optional

from telegram import Update
from telegram.ext import MessageHandler, ContextTypes
from telegram.ext import filters

from lib import melman_logging
from lib.melman_errors import MelmanInvalidEndpoint
from lib.resolver.melman_help import MelmanHelp
from lib.resolver.melman_router import MelmanRouter
from lib.resolver.melman_types import MelmanApp
from lib.resolver.melman_update import MelmanUpdate

logger = melman_logging.get_logger("MelmanModule")


class MelmanModule(MelmanRouter):
    """
    The base module for Melman modules.

    Allows you to create a simple and straightforward route-based command-response program.
    """

    def __init__(self, module_name: str, help_msg: Optional[MelmanHelp] = None) -> None:
        super().__init__()
        self.help = help_msg
        self.module_name = module_name

    async def _routing_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Get the route we're supposed to navigate to.
        """
        melman_update = MelmanUpdate(self.module_name, update)

        path = melman_update.get_path()

        try:
            target = self.lookup_route(self.module_name, path)
        except MelmanInvalidEndpoint:
            logger.error(f"{self.module_name}: Could not resolve '{path}'")
            return await self.send_help_message_to_user(melman_update)

        logger.info(f"{self.module_name}: Resolved '{path}'")
        await target(melman_update, context)

    async def send_help_message_to_user(self, update: MelmanUpdate) -> None:
        """
        Print the help menu to the user, if there is one.
        """
        if not self.help:
            return

        await self.help.send_help_message(update)

    def register_module(self, telegram_app: MelmanApp) -> None:
        logger.info(f"Registering '{self.module_name}' module")
        handler = MessageHandler(filters=filters.Regex('^' + self.module_name), callback=self._routing_callback)
        telegram_app.add_handler(handler)
