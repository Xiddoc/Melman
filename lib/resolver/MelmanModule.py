from typing import Callable

from http_router import Router
from http_router.router import TPath, TVObj
from telegram import Update
from telegram.ext import Application, CallbackContext, MessageHandler
from telegram.ext import filters
# noinspection PyProtectedMember
from telegram.ext._utils.types import HandlerCallback, CCT, RT

MelmanCallback = HandlerCallback[Update, CCT, RT]
MelmanDecoratorWrapper = Callable[[MelmanCallback], TVObj]
MelmanRoutes = TPath

COMMAND_DELIMETER = " "


# logger = melman_logger.get_logger("MelmanModule")

class MelmanRouter(Router):
    """
    A slightly improved router.
    Wraps the routing functionality.
    """

    def route(self, *paths: MelmanRoutes, **opts) -> MelmanDecoratorWrapper:
        if not paths:
            # Empty route
            paths = ('',)

        return super().route(*paths, **opts)

    def lookup_route(self, path: str) -> MelmanCallback:
        return self.__call__(path).target


class MelmanModule(MelmanRouter):
    """
    The base module for Melman modules.

    Allows you to create a simple and straightforward route-based command-response program.
    """

    def __init__(self, module_name: str) -> None:
        super().__init__()
        self.module_name = module_name

    async def _routing_callback(self, update: Update, context: CallbackContext) -> None:
        """
        Get the route we're supposed to navigate to.
        """
        path = self._get_path_from_update(update)

        target = self.lookup_route(path)

        await target(update, context)

    def _get_path_from_update(self, update: Update) -> str:
        original_path = update.message.text or update.message.caption

        path_arguments = original_path.removeprefix(self.module_name).strip()

        first_argument, *_ = path_arguments.split(COMMAND_DELIMETER, 1)

        return first_argument

    def register_module(self, telegram_app: Application) -> None:
        # logger.info(f"Registering '{self.module_name}' module")
        handler = MessageHandler(filters=filters.Regex('^' + self.module_name), callback=self._routing_callback)
        telegram_app.add_handler(handler)
