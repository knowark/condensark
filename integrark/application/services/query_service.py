from abc import ABC, abstractmethod
from typing import Dict, Any


class QueryService(ABC):
    """Query service."""

    @abstractmethod
    async def run(self, query: str) -> None:
        """Run query string"""


class StandardQueryService(QueryService):

    def __init__(self, response=None) -> None:
        self.response = response or {}

    async def run(self, query: str) -> Dict[str, Any]:
        return self.response
