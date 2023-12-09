"""
The list of modules ready for public usage.
"""
from typing import List

from lib import MelmanModule
from modules.hello_world.hello_world import hello_world

MELMAN_MODULES: List[MelmanModule] = [
    hello_world
]
