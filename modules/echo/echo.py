"""
An echo command! Echo, echo, echo...
"""
import re

from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp

echo = MelmanModule("echo", help_msg=MelmanMDHelp("""
**`echo`**
Echos data back to the chat.

**Usage**
```telegram
echo <TEXT>
```
"""))


# noinspection PyUnusedFunction
@echo.route(re.compile(r".+"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.get_path())
