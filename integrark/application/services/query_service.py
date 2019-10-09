from abc import ABC, abstractmethod
from typing import Any, Dict, NamedTuple


QueryResult = NamedTuple('QueryResult', [('data', Any), ('errors', Any)])

Context = Dict[str, Any]


class QueryService(ABC):
    """Query service."""

    @abstractmethod
    async def run(self, query: str, context: Context = None) -> QueryResult:
        """Run query string"""


class StandardQueryService(QueryService):

    def __init__(self, response=None) -> None:
        self.response = response or QueryResult(None, None)

    async def run(self, query: str, context: Context = None) -> QueryResult:
        return self.response
