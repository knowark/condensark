from abc import ABC, abstractmethod
from typing import Dict, Any


QueryResult = Dict[str, Any]


class QueryService(ABC):
    """Query service."""

    @abstractmethod
    async def run(self, query: str) -> QueryResult:
        """Run query string"""


class StandardQueryService(QueryService):

    def __init__(self, response=None) -> None:
        self.response = response or {}

    async def run(self, query: str) -> QueryResult:
        return self.response
