"""
Run a shodan query.
"""
import re

from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp
from modules.shodan.shodan_query import Shodan

shodan_cmd = MelmanModule("shodan", help_msg=MelmanMDHelp("""
**`shodan`**
Run a Shodan query.
"""))

shodan_query = Shodan()


# noinspection PyUnusedFunction
@shodan_cmd.route(re.compile(".+"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.get_path()

    results = shodan_query.search(query)

    await update.message.reply_text(str(results))
