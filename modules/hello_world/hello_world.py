from telegram import Update
from telegram.ext import ContextTypes

from lib import MelmanModule

hello_world = MelmanModule("helloworld")


# noinspection PyUnusedFunction
@hello_world.route()
async def index(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(update.message.text)
