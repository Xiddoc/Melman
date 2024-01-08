"""
The list of modules ready for public usage.
"""
from typing import List

from lib import MelmanModule
from modules.echo.echo import echo
from modules.hello_world.hello_world import hello_world
from modules.help_command.help_command import help_cmd
from modules.hypixel.hypixel import hypixel
from modules.mcserv.mcserv import mcserv
from modules.shodan.shodan import shodan_cmd

MELMAN_MODULES: List[MelmanModule] = [
    hello_world,
    echo,
    help_cmd,
    hypixel,
    mcserv,
    shodan_cmd
]
