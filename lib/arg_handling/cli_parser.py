"""
The CLI argument parser.
"""
import argparse

from lib.arg_handling.arg_handler import MELMAN_COMMAND_ARG
from lib.commons.melman_config import AUTO_UPDATE_PARAM, AUTO_UPDATE_DEFAULT


def get_parser() -> argparse.ArgumentParser:
    """
    Builds the ArgumentParser object and returns it.
    """
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(required=True, dest=MELMAN_COMMAND_ARG,
                                      help="The different actions that the Melman runner program can perform.")

    start = subparser.add_parser("start",
                                 help="Start the Melman bot and run synchronously until termination or exception.")
    start.add_argument("--" + AUTO_UPDATE_PARAM,
                       action=argparse.BooleanOptionalAction,
                       default=AUTO_UPDATE_DEFAULT)

    subparser.add_parser("update",
                         help="Update the Melman bot on demand. Melman will also auto-update himself periodically.")

    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()
