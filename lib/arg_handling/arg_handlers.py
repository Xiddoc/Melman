from abc import abstractmethod, ABCMeta
from typing import Type, Dict, Any

from lib.commons.melman_config import REMOTE_GIT_LINK, AUTO_UPDATE_PARAM
from lib.keys.token_loader import TokenLoader
from lib.resolver.melman_core import MelmanCore
from lib.updater.melman_updater import MelmanUpdater


class MelmanArgumentHandler(metaclass=ABCMeta):
    """
    The base class for argument handlers for the CLI parsing logic.
    """

    @classmethod
    @abstractmethod
    def handle(cls, *args: Any, **kwargs: Any) -> None:
        """
        The function which is called when executed.
        """


class StartMelman(MelmanArgumentHandler):
    """
    Start the Melman bot synchronously.
    """

    @classmethod
    def handle(cls, *args: Any, **kwargs: Any) -> None:
        melman = MelmanCore(TokenLoader.get_token(),
                            update_git_repo_url=REMOTE_GIT_LINK,
                            auto_update=kwargs[AUTO_UPDATE_PARAM])
        melman.start()


class UpdateMelman(MelmanArgumentHandler):
    """
    Update Melman from the remote Git repo.
    """

    @classmethod
    def handle(cls, *args: Any, **kwargs: Any) -> None:
        updater = MelmanUpdater(REMOTE_GIT_LINK)
        updater.update()


ARG_HANDLERS: Dict[str, Type[MelmanArgumentHandler]] = {
    "start": StartMelman,
    "update": UpdateMelman
}
