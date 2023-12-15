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

## Examples

All that talk is great and all, but let's see it for ourselves with some friendly
snippets of code to guide us through the process of making our own Melman module. 

### Basic module

In the below code snippet, you can see just how easy it is to make an `echo` command
which responds to all text (using the `.+` RegEx):

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

### Set default module behavior

If a user only types your modules name without any parameters, then one of two things can happen:
- You could resolve the empty route to your own function and handle it
- You could leave it alone and instead set up a help menu to be printed

In this example, we will see how to add a help menu to our previous `echo` command. 
All that must be done is to add the `help` parameter to the module constructor:

```python
from lib import MelmanModule, MelmanMDHelp

echo = MelmanModule("echo", help_msg=MelmanMDHelp("""
**`echo`**
Echos data back to the chat.

Usage: `echo <TEXT>`
"""))
```

In the above example, we selected the `MelmanMDHelp` source so that we can display MarkDown
formatting for our help menu. However, we also have other "help types" that we can use, 
such as plain old text using the `MelmanTextHelp` type:

```python
from lib import MelmanModule, MelmanTextHelp

echo = MelmanModule("echo", help_msg=MelmanTextHelp("""
The *echo* command.
Echos whatever you say right back at it!
"""))
```

This time, the asteriks in the help text (around the word "echo") will not be turned to markdown
formatting for the text.

## Setup
Add a `.env` file or add an environment variable with your Telegram bot key, generated via BotFather, like so:
```.env
TELEGRAM_API_KEY=12345:ABCDEFGGGGGGGGGGGGGGGGGGGGGG
```

## License
See the [LICENSE](LICENSE) file.