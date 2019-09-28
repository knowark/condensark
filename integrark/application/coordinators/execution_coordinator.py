from typing import Dict, Any
from ..services import QueryService


class ExecutionCoordinator:
    def __init__(self, query_service: QueryService) -> None:
        self.query_service = query_service

    async def execute(self, query: str) -> Dict[str, Any]:
        result = await self.query_service.run(query)

        return result
