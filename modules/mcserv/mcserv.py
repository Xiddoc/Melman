"""
Get the server IP
"""

from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp

mcserv = MelmanModule("mcserv", help_msg=MelmanMDHelp("""
**`mcserv`**
Gets the IP of the MC serv.
"""))


# noinspection PyUnusedFunction
@mcserv.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.get_path())
