<!--suppress HtmlDeprecatedAttribute -->
<p align="center">
<img width=100 height=100 src=https://cdn-icons-png.flaticon.com/512/848/848698.png  alt="Melman">
</p>

# Melman
A route-based modular Telegram bot.

---

## Introduction

Most Telegram bots are heavily function-based, and are based on global events
that are often triggered for all the functions at the same time. Melman puts an end to that.
Now, route-based modularity is achieved with a similar interface to that of your favorite
web server.

Let's see an example:

```python
import re
from telegram.ext import ContextTypes
from lib import MelmanModule, MelmanUpdate

echo = MelmanModule("echo")


@echo.route(re.compile(r".+"))
async def index(update: MelmanUpdate, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.get_path())
```

The `echo` command in most systems behaves by taking an input it is given and reflecting 
it back to the screen. Similarly, all you have to do to create a command with Melman is to
register your route with `MelmanModule`, then describe your route- which even supports 
Regular Expressions, as can be seen with the `re.compile(r".+")` expression.

## Setup
Add a `.env` file or add an environment variable with your Telegram bot key, generated via BotFather, like so:
```.env
TELEGRAM_API_KEY=12345:ABCDEFGGGGGGGGGGGGGGGGGGGGGG
```

## License
See the [LICENSE](LICENSE) file.