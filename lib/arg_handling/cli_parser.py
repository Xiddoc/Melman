"""
The CLI argument parser.
"""
import argparse

from lib.arg_handling.arg_handler import MELMAN_COMMAND_ARG


def get_parser() -> argparse.ArgumentParser:
    """
    Builds the ArgumentParser object and returns it.
    """
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(required=True, dest=MELMAN_COMMAND_ARG,
                                      help="The different actions that the Melman runner program can perform.")
    subparser.add_parser("start",
                         help="Start the Melman bot and run synchronously until termination or exception.")

    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()
