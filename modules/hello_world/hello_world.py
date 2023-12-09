from telegram.ext import ContextTypes

from lib import MelmanModule
from lib.resolver.MelmanModule import MelmanUpdate

hello_world = MelmanModule("helloworld")


# noinspection PyUnusedFunction
@hello_world.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.get_text():
        return

    await update.message.reply_text(update.get_text())
