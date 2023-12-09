from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate
from lib.resolver.melman_help import MelmanTextHelp

hello_world = MelmanModule("helloworld", help_msg=MelmanTextHelp("Prints a basic hello world message to the screen!"))


# noinspection PyUnusedFunction
@hello_world.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text("Hey, I'm Melman, your favorite giraffe Telegram bot!")
