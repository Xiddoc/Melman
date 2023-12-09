from telegram import Update
from telegram.ext import CallbackContext

from lib import MelmanModule

hello_world = MelmanModule("helloworld")


@hello_world.route()
async def index(update: Update, context: CallbackContext):
    await update.message.reply_text("Hey, I'm Melman, your favorite giraffe Telegram bot!")
