"""
The CLI argument parser.
"""
import argparse


def get_parser() -> argparse.ArgumentParser:
    """
    Builds the ArgumentParser object and returns it.
    """
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(required=True,
                                      help="The different actions that the Melman runner program can perform.")
    subparser.add_parser("start",
                         help="Start the Melman bot and run synchronously until termination or exception.")

    return parser


def parse_args() -> argparse.Namespace:
    return get_parser().parse_args()
