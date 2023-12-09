"""
The list of modules ready for public usage.
"""
from typing import List

from lib import MelmanModule
from modules.download.download import download
from modules.echo.echo import echo
from modules.hello_world.hello_world import hello_world
from modules.help_command.help_command import help_cmd

MELMAN_MODULES: List[MelmanModule] = [
    hello_world,
    echo,
    help_cmd,
    download
]
