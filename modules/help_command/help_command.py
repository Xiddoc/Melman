import re
from typing import List, Optional

from telegram.ext import ContextTypes

from lib import MelmanModule, MelmanUpdate, MelmanMDHelp

BASE_HELP_TEXT = """
*Melman - Your bot for quick and simple tasks*

To see all commands, type:
```telegram
help
```

To see information about a specific command, type:
```telegram
help <COMMAND_NAME>
```

"""

help_cmd = MelmanModule("help", MelmanMDHelp(BASE_HELP_TEXT))


# noinspection PyUnusedFunction
@help_cmd.route()
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    from modules import MELMAN_MODULES

    help_text = BASE_HELP_TEXT + "Available commands:\n"

    for module in MELMAN_MODULES:
        help_text += f"• `{module.module_name}`\n"

    await MelmanMDHelp(help_text).send_help_message(update)


# noinspection PyUnusedFunction
@help_cmd.route(re.compile(r".+"))
async def get_specific_command_help(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    from modules import MELMAN_MODULES

    module = get_module_by_name(update.get_path(), MELMAN_MODULES)

    if not module:
        await update.message.reply_text("No command inputted.")
        return

    await module.send_help_message_to_user(update)


def get_module_by_name(module_name: str, modules: List[MelmanModule]) -> Optional[MelmanModule]:
    for module in modules:
        if module.module_name == module_name:
            return module

    return None
