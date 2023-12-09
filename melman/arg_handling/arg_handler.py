"""
Different logic flow based on the inputted CLI arguments.
The start of the different flows is parsed here then sent off to different logic handlers deeper into the code.
"""
import argparse
from typing import Type

from melman.arg_handling.arg_handlers import ARG_HANDLERS, MelmanArgumentHandler

MELMAN_COMMAND_ARG = 'command'


def _unsafe_get_handler(inputted_command: str) -> Type[MelmanArgumentHandler]:
    return ARG_HANDLERS[inputted_command]


def get_handler(inputted_command: str) -> Type[MelmanArgumentHandler]:
    try:
        return _unsafe_get_handler(inputted_command)
    except KeyError:
        raise argparse.ArgumentError(None, f"Could not find command '{inputted_command}'.")


def handle_parsed_args(cli_args: argparse.Namespace) -> None:
    cli_args

