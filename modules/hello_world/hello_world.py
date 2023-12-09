from telegram import Update

from lib import MelmanModule

hello_world = MelmanModule("helloworld")


# noinspection PyUnusedFunction
@hello_world.route()
async def index(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)
