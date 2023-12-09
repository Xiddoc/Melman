from telegram import Update
from telegram.ext import MessageHandler, ContextTypes
from telegram.ext import filters

from lib.melman_errors import MelmanInvalidEndpoint
from lib.melman_logging import logger
from lib.resolver.melman_router import MelmanRouter
from lib.resolver.melman_types import MelmanApp
from lib.resolver.melman_update import MelmanUpdate


class MelmanModule(MelmanRouter):
    """
    The base module for Melman modules.

    Allows you to create a simple and straightforward route-based command-response program.
    """

    def __init__(self, module_name: str) -> None:
        super().__init__()
        self.module_name = module_name

    async def _routing_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Get the route we're supposed to navigate to.
        """
        melman_update = MelmanUpdate.from_update(update)

        path = self._get_path_from_update(melman_update)

        try:
            target = self.lookup_route(self.module_name, path)
        except MelmanInvalidEndpoint:
            # Endpoint was not found
            # Essentially a 404 page
            logger.error(f"{self.module_name}: Could not resolve '{path}'")
            return

        logger.info(f"{self.module_name}: Resolved '{self.path}'")
        await target(melman_update, context)

    def _get_path_from_update(self, update: MelmanUpdate) -> str:
        """
        Get the route we're supposed to call, given the message.
        For example, given 'echo 1 2 3' we should return '1 2 3'.
        """
        original_path = update.get_text()

        if not original_path:
            return ''

        path_arguments = original_path.removeprefix(self.module_name).strip()

        return path_arguments

    def register_module(self, telegram_app: MelmanApp) -> None:
        logger.info(f"Registering '{self.module_name}' module")
        handler = MessageHandler(filters=filters.Regex('^' + self.module_name), callback=self._routing_callback)
        telegram_app.add_handler(handler)
