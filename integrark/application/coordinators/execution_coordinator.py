from typing import Dict, Any
from ..services import QueryService, QueryResult


class ExecutionCoordinator:
    def __init__(self, query_service: QueryService) -> None:
        self.query_service = query_service

    async def execute(self, query: str,
                      context: Dict[str, Any] = None) -> Dict[str, Any]:

        result = await self.query_service.run(query, context)

        response: Dict[str, Any] = {}

        if result.errors:
            response['errors'] = result.errors

        if result.data:
            response['data'] = result.data

        return response
