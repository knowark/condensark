from typing import List, Dict, Any
from ....application.services import RouteService
from ...core import IntegrationImporter, Location


class RestRouteService(RouteService):

    def __init__(self, integration_importer: IntegrationImporter) -> None:
        self.locations: Dict[str, Location] = {
            location.path: location
            for location in integration_importer.locations}

    async def route(self, location: str,
                    context: Dict[str, Any] = None) -> Any:
        context = context or {}

        route = self.locations[location].route

        return await route(context)
