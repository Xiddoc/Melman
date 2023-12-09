from typing import Optional

from telegram import Update


class MelmanUpdate(Update):
    def __init__(self, update: Update) -> None:
        super().__init__(update.update_id)

    def get_text(self) -> Optional[str]:
        if not self.message:
            return None

        return self.message.text or self.message.caption