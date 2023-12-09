"""
The root handler for the Bot, which passes the rest of the logic onto other components.
"""
import asyncio

import telegram


class MelmanCore:

    def __init__(self, api_token: str) -> None:
        self._api_key = api_token

    def start(self) -> None:
        asyncio.run(self._main_flow())

    async def _main_flow(self):
        bot = telegram.Bot(self._api_key)

        async with bot:
            print(await bot.get_me())
