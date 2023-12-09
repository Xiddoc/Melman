from typing import cast

from telegram import Update

EMPTY_STRING = ''


class MelmanUpdate(Update):

    def get_text(self) -> str:
        if not self.message:
            return EMPTY_STRING

        return \
            self.message.text \
            or self.message.caption \
            or EMPTY_STRING

    @staticmethod
    def from_update(update: Update) -> "MelmanUpdate":
        """
        Get a MelmanUpdate object from a Telegram update object.
        """
        update.__class__ = MelmanUpdate

        return cast(MelmanUpdate, update)
