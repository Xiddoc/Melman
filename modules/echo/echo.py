"""
An echo command! Echo, echo, echo...
"""
import re

from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate

echo = MelmanModule("echo")


# noinspection PyUnusedFunction
@echo.route(re.compile(r".*"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await update.message.reply_text(update.get_path())
