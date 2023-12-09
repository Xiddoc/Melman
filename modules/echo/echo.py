"""
An echo command! Echo, echo, echo...
"""
from telegram import Update
from telegram.ext import ContextTypes

from lib import MelmanModule

echo = MelmanModule("echo")


# noinspection PyUnusedFunction
@echo.route()
async def index(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text("Hey, I'm Melman, your favorite giraffe Telegram bot!")
