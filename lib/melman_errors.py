"""
General errors that Melman can encounter.
All errors should stem from MelmanError.
"""


class MelmanError(Exception):
    """
    The base exception for all Melman exceptions.
    """


class MelmanStartupError(MelmanError):
    """
    Melman could not even get himself off the ground (start up until successful program smooth flow).
    """
