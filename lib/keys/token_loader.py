import os

from dotenv import load_dotenv

from lib import melman_config, melman_errors


class TokenLoader:

    @classmethod
    def get_token(cls) -> str:
        """
        Retrieves the Telegram API token to use for the bot.

        :return: The Telegram Bot's API token.
        """
        cls._load_tokens_to_memory()

        try:
            return cls._unsafe_get_token()
        except KeyError as exc:
            raise melman_errors.MelmanStartupError(f"No API key found at '{melman_config.API_KEY_NAME}'.") from exc

    @staticmethod
    def _load_tokens_to_memory() -> None:
        load_dotenv()

    @staticmethod
    def _unsafe_get_token() -> str:
        """
        :raises KeyError: If the API key is not found.
        """
        return os.environ[melman_config.API_KEY_NAME]
