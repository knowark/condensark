from pathlib import Path
from ...application.services import (
    QueryService, StandardQueryService,
    RouteService, StandardRouteService)
from ...application.managers import (
    ExecutionManager, RoutingManager)
from ..core import Config, JwtSupplier, IntegrationImporter
from .factory import Factory


class MemoryFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def standard_query_service(self) -> StandardQueryService:
        return StandardQueryService()

    def standard_route_service(self) -> StandardRouteService:
        return StandardRouteService()

    def execution_manager(
            self, query_service: QueryService) -> ExecutionManager:
        return ExecutionManager(query_service)

    def routing_manager(
            self, route_service: RouteService) -> RoutingManager:
        return RoutingManager(route_service)

    def jwt_supplier(self) -> JwtSupplier:
        secret_file = Path(self.config.get('secrets', {}).get('jwt', ''))
        secret = (secret_file.read_text().strip()
                  if secret_file.is_file() else 'INTEGRARK_SECRET')

        return JwtSupplier(secret)

    def integration_importer(self) -> IntegrationImporter:
        integrations_directory = self.config['integrations_directory']
        integration_importer = IntegrationImporter(integrations_directory)
        integration_importer.load()
        return integration_importer
