from enum import Enum

from lib.resolver.melman_update import MelmanUpdate

REPLY_FUNCTION_NAME_PREFIX = "reply_"


class MelmanHelpTextType(Enum):
    MD = 'markdown_v2'
    TEXT = 'text'


class MelmanHelp:

    def __init__(self, help_txt: str, text_type: MelmanHelpTextType) -> None:
        self.help_txt = help_txt
        self.text_type = text_type

    def send_help_message(self, update: MelmanUpdate) -> None:
        """
        Send the help message to the user.
        """
        reply_function = getattr(update.message, self._get_reply_function_name())
        reply_function(self.help_txt)

    def _get_reply_function_name(self) -> str:
        """
        Get the name of the reply function to use, given the help message type.

        For example, MD help messages should return `reply_markdown_v2`.
        """
        return REPLY_FUNCTION_NAME_PREFIX + str(self.text_type.value)


class MelmanMDHelp(MelmanHelp):
    def __init__(self, help_txt: str):
        super().__init__(help_txt, MelmanHelpTextType.MD)


class MelmanTextHelp(MelmanHelp):
    def __init__(self, help_txt: str):
        super().__init__(help_txt, MelmanHelpTextType.TEXT)
