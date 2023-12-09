from abc import abstractmethod, ABCMeta
from typing import Type, Dict

from lib.core.melman_core import MelmanCore
from lib.keys.token_loader import TokenLoader


class MelmanArgumentHandler(metaclass=ABCMeta):
    """
    The base class for argument handlers for the CLI parsing logic.
    """

    @classmethod
    @abstractmethod
    def handle(cls, *args: str, **kwargs: str) -> None:
        """
        The function which is called when executed.
        """


class StartMelman(MelmanArgumentHandler):
    """
    Start the Melman bot synchronously.
    """

    @classmethod
    def handle(cls, *args: str, **kwargs: str) -> None:
        melman = MelmanCore(TokenLoader.get_token())
        melman.start()


ARG_HANDLERS: Dict[str, Type[MelmanArgumentHandler]] = {
    "start": StartMelman
}
