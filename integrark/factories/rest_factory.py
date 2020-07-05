from ..core import Config, IntegrationImporter
from ..core.route import RestRouteService
from .memory_factory import MemoryFactory


class RestFactory(MemoryFactory):
    def __init__(self, config: Config) -> None:
        self.config = config

    def rest_route_service(
            self, integration_importer: IntegrationImporter
    ) -> RestRouteService:
        return RestRouteService(integration_importer)
