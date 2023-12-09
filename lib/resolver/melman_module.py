from typing import Callable, Any, Coroutine

from http_router.router import TPath, TVObj
from telegram import Update
from telegram.ext import Application, CallbackContext, MessageHandler
from telegram.ext import filters

from lib.resolver.melman_router import MelmanRouter
from lib.resolver.melman_update import MelmanUpdate

COMMAND_DELIMETER = " "

MelmanHandlerReturnType = None
MelmanHandlerContext = CallbackContext
MelmanRoutes = TPath
MelmanCallback = Callable[[MelmanUpdate, MelmanHandlerContext], Coroutine[Any, Any, MelmanHandlerReturnType]]
MelmanDecoratorWrapper = Callable[[MelmanCallback], TVObj]


# logger = melman_logger.get_logger("MelmanModule")


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
        melman_update = MelmanUpdate(update)

        path = self._get_path_from_update(melman_update)

        target = self.lookup_route(path)

        await target(update, context)

    def _get_path_from_update(self, update: MelmanUpdate) -> str:
        """
        Get the route we're supposed to call, given the message.
        """
        original_path = update.get_text()

        if not original_path:
            return ''

        path_arguments = original_path.removeprefix(self.module_name).strip()

        first_argument, *_ = path_arguments.split(COMMAND_DELIMETER, 1)

        return first_argument

    def register_module(self, telegram_app: Application) -> None:
        # logger.info(f"Registering '{self.module_name}' module")
        handler = MessageHandler(filters=filters.Regex('^' + self.module_name), callback=self._routing_callback)
        telegram_app.add_handler(handler)
