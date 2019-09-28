from ...application.services import QueryService, StandardQueryService
from ...application.coordinators import ExecutionCoordinator
from ..core import Config
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def standard_query_service(self) -> StandardQueryService:
        return StandardQueryService()

    def execution_coordinator(
            self, query_service: QueryService) -> ExecutionCoordinator:
        return ExecutionCoordinator(query_service)
