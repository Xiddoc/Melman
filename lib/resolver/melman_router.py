from typing import cast, Any

from http_router import Router, NotFoundError

from lib.melman_errors import MelmanInvalidEndpoint
from lib.resolver.melman_types import MelmanRoutes, MelmanCallback, MelmanDecoratorWrapper


class MelmanRouter(Router):
    """
    A slightly improved router.
    Wraps the routing functionality.
    """

    def route(self, *paths: MelmanRoutes, **opts: Any) -> MelmanDecoratorWrapper:
        if not paths:
            # Empty route
            paths = ('',)

        return super().route(*paths, **opts)

    def lookup_route(self, module_name: str, path: str) -> MelmanCallback:
        """
        :raises MelmanInvalidEndpoint: If the endpoint doesn't exist.
        """
        try:
            return self._unsafe_lookup_route(path)
        except NotFoundError as exc:
            raise MelmanInvalidEndpoint(module_name, path) from exc

    def _unsafe_lookup_route(self, path: str) -> MelmanCallback:
        """
        :raises http_router.NotFoundError: If the endpoint doesn't exist.
        """
        return cast(MelmanCallback, self.__call__(path).target)
