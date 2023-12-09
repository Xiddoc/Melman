from melman.arg_handling import cli_parser
from melman.arg_handling.arg_handler import handle_parsed_args


def handle_args() -> None:
    args = cli_parser.parse_args()
    handle_parsed_args(args)
