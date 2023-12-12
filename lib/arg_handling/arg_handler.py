"""
Different logic flow based on the inputted CLI arguments.
The start of the different flows is parsed here then sent off to different logic handlers deeper into the code.
"""
import argparse
from typing import Type, Dict

from lib import melman_logging
from lib.arg_handling.arg_handlers import ARG_HANDLERS, MelmanArgumentHandler
from lib.melman_banner import MELMAN_BANNER
from lib.melman_errors import MelmanError

MELMAN_COMMAND_ARG = 'command'
logger = melman_logging.get_logger("Melman")


def _unsafe_get_handler(inputted_command: str) -> Type[MelmanArgumentHandler]:
    return ARG_HANDLERS[inputted_command]


def get_handler(inputted_command: str) -> Type[MelmanArgumentHandler]:
    try:
        return _unsafe_get_handler(inputted_command)
    except KeyError:
        raise argparse.ArgumentError(None, f"Could not find command '{inputted_command}'.")


def get_arguments_as_dict(cli_args: argparse.Namespace) -> Dict[str, str]:
    return vars(cli_args)


def handle_parsed_args(cli_args: argparse.Namespace) -> None:
    command: str = getattr(cli_args, MELMAN_COMMAND_ARG)

    handler = get_handler(command)
    arguments = get_arguments_as_dict(cli_args)

    try:
        print(MELMAN_BANNER)
        handler.handle(**arguments)
    except MelmanError as exc:
        logger.error("Unexpected error occurred:")
        logger.error(exc)
