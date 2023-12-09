from telegram import Update

EMPTY_STRING = ''


class MelmanUpdate(Update):
    _module_name: str

    def __init__(self, module_name: str, update: Update) -> None:
        """
        Get a MelmanUpdate object from a Telegram update object.
        """
        super(Update, self).__init__()

        self._module_name = module_name
        self._copy_other_attributes_to_self(update)

    def get_path(self) -> str:
        """
        Get the route that this update calls.
        For example, given the update message `echo 1 2 3`, we should return `1 2 3`.
        """
        original_path = self.get_text()

        if not original_path:
            return ''

        path_arguments = original_path.removeprefix(self._module_name).strip()

        return path_arguments

    def get_text(self) -> str:
        if not self.message:
            return EMPTY_STRING

        return \
            self.message.text \
            or self.message.caption \
            or EMPTY_STRING

    def _copy_other_attributes_to_self(self, other: object) -> None:
        for attribute in other.__slots__:
            setattr(self, attribute, getattr(other, attribute))

    def __setattr__(self, key: str, value: object) -> None:
        super(Update, self).__setattr__(key, value)
