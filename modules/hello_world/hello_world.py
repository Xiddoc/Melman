from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanTextHelp

hello_world = MelmanModule("helloworld", help_msg=MelmanTextHelp("Prints a basic hello world message to the screen!"))


# noinspection PyUnusedFunction
@hello_world.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hey, I'm Melman, your favorite giraffe Telegram bot!")
