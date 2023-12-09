from typing import Union, Pattern, Callable, Coroutine, Any, Dict

from telegram.ext import Application, CallbackContext, JobQueue, ExtBot

from lib.resolver.melman_update import MelmanUpdate

MelmanHandlerContext = CallbackContext[ExtBot[None],
                                       Dict[Any, Any],
                                       Dict[Any, Any],
                                       Dict[Any, Any]]
MelmanRoutes = Union[str, Pattern]
MelmanCallback = Callable[[MelmanUpdate, MelmanHandlerContext], Coroutine[Any, Any, None]]
MelmanDecoratorWrapper = Callable[[MelmanCallback], Any]
MelmanApp = Application[ExtBot[None],
                        MelmanHandlerContext,
                        Dict[Any, Any],
                        Dict[Any, Any],
                        Dict[Any, Any],
                        JobQueue[MelmanHandlerContext]]
