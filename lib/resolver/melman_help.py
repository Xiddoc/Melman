from typing import Optional

from telegram.constants import ParseMode

from lib.resolver.melman_update import MelmanUpdate


class MelmanHelp:

    def __init__(self, help_txt: str, format_type: Optional[ParseMode]) -> None:
        self.help_txt = help_txt
        self.text_type = format_type

    async def send_help_message(self, update: MelmanUpdate) -> None:
        """
        Send the help message to the user.
        """
        await update.message.reply_text(self.help_txt, parse_mode=self.text_type)


class MelmanMDHelp(MelmanHelp):
    BLACKLIST = ['#', '.', '>', '<', '-', '!']

    def __init__(self, help_txt: str):
        super().__init__(self._escape_md(help_txt), format_type=ParseMode.MARKDOWN_V2)

    @classmethod
    def _escape_md(cls, message: str) -> str:
        for blacklisted_char in cls.BLACKLIST:
            message = message.replace(blacklisted_char, '\\' + blacklisted_char)

        return message


class MelmanTextHelp(MelmanHelp):
    def __init__(self, help_txt: str):
        super().__init__(help_txt, format_type=None)
