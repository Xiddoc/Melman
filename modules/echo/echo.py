"""
An echo command! Echo, echo, echo...
"""
from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate

echo = MelmanModule("echo")


# noinspection PyUnusedFunction
@echo.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(update.get_text())
