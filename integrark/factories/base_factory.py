from pathlib import Path
from injectark import Factory
from ..application.services import (
    QueryService, StandardQueryService,
    RouteService, StandardRouteService)
from ..application.managers import (
    ExecutionManager, RoutingManager)
from ..core import Config, JwtSupplier, IntegrationImporter


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def query_service(
            self, integration_importer: IntegrationImporter) -> QueryService:
        return StandardQueryService()

    def route_service(
            self, integration_importer: IntegrationImporter) -> RouteService:
        return StandardRouteService()

    def execution_manager(
            self, query_service: QueryService) -> ExecutionManager:
        return ExecutionManager(query_service)

    def routing_manager(
            self, route_service: RouteService) -> RoutingManager:
        return RoutingManager(route_service)

    def jwt_supplier(self) -> JwtSupplier:
        secret = self.config.get('secrets', {}).get('jwt', '')
        return JwtSupplier(secret)

    def integration_importer(self) -> IntegrationImporter:
        integrations_directory = self.config['integrations_directory']
        integration_importer = IntegrationImporter(integrations_directory)
        integration_importer.load()
        return integration_importer
