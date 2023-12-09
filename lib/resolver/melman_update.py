from telegram import Update

EMPTY_STRING = ''


class MelmanUpdate(Update):
    def __init__(self, update: Update) -> None:
        super().__init__(update.update_id)

    def get_text(self) -> str:
        if not self.message:
            return EMPTY_STRING

        return \
            self.message.text \
            or self.message.caption \
            or EMPTY_STRING
