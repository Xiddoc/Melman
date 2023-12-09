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

