from ..application.services import RouteService
from ..core import Config, IntegrationImporter
from ..core.route import RestRouteService
from .base_factory import BaseFactory


class RestFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def route_service(
            self, integration_importer: IntegrationImporter
    ) -> RouteService:
        return RestRouteService(integration_importer)
