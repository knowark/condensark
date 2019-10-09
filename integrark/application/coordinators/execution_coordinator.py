from typing import Dict, Any
from ..services import QueryService, QueryResult


class ExecutionCoordinator:
    def __init__(self, query_service: QueryService) -> None:
        self.query_service = query_service

    async def execute(self, query: str,
                      context: Dict[str, Any] = None) -> QueryResult:

        result = await self.query_service.run(query, context)

        return result
