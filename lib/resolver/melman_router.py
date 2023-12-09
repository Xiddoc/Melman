from typing import cast

from http_router import Router

from lib.resolver.melman_module import MelmanRoutes, MelmanDecoratorWrapper, MelmanCallback


class MelmanRouter(Router):
    """
    A slightly improved router.
    Wraps the routing functionality.
    """

    def route(self, *paths: MelmanRoutes, **opts) -> MelmanDecoratorWrapper:
        if not paths:
            # Empty route
            paths = ('',)

        return super().route(*paths, **opts)

    def lookup_route(self, path: str) -> MelmanCallback:
        return cast(MelmanCallback, self.__call__(path).target)