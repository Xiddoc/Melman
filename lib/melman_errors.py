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


class MelmanModuleError(MelmanError):
    """
    An error that Melman encountered in the processing of a module.
    """

    def __init__(self, module_name: str, message: str) -> None:
        self.module_name = module_name
        self.message = message

    def __str__(self) -> str:
        return f"Error in module '{self.module_name}': {self.message}"


class MelmanInvalidEndpoint(MelmanModuleError):
    def __init__(self, module_name: str, endpoint: str):
        super().__init__(module_name, f"Endpoint was accessed but does not exist: {endpoint}")
