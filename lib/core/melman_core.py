"""
The root handler for the Bot, which passes the rest of the logic onto other components.
"""
import asyncio

import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from lib.melman_banner import MELMAN_BANNER


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


class MelmanCore:

    def __init__(self, api_token: str) -> None:
        self._api_key = api_token

    def start(self) -> None:
        print(MELMAN_BANNER)
        self._main_flow()
        # asyncio.run(self._main_flow())

    def _main_flow(self) -> None:
        application = ApplicationBuilder().token(self._api_key).build()

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        application.run_polling()

        # async with bot:
        #     print(await bot.get_updates())
