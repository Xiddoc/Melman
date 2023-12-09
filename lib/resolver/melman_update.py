from typing import cast

from telegram import Update

EMPTY_STRING = ''


class MelmanUpdate(Update):
    module_name: str
    __slots__ = tuple()

    def get_path(self) -> str:
        """
        Get the route that this update calls.
        For example, given the update message `echo 1 2 3`, we should return `1 2 3`.
        """
        original_path = self.get_text()

        if not original_path:
            return ''

        path_arguments = original_path.removeprefix(self.module_name).strip()

        return path_arguments

    def get_text(self) -> str:
        if not self.message:
            return EMPTY_STRING

        return \
            self.message.text \
            or self.message.caption \
            or EMPTY_STRING

    @staticmethod
    def from_update(module_name: str, update: Update) -> "MelmanUpdate":
        """
        Get a MelmanUpdate object from a Telegram update object.
        """
        update.__class__ = MelmanUpdate

        melman_update = cast(MelmanUpdate, update)
        melman_update.module_name = module_name

        return melman_update
