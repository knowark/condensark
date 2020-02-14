from abc import ABC, abstractmethod
from typing import Any, Dict


Context = Dict[str, Any]


class RouteService(ABC):
    """Query service."""

    @abstractmethod
    async def route(self, location: str, context: Context = None) -> Any:
        """Route location."""


class StandardRouteService(RouteService):

    def __init__(self, response=None) -> None:
        self.response = response

    async def route(self, location: str,
                    context: Context = None) -> Any:
        return self.response
