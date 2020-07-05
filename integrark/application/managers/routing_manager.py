from typing import Dict, Any
from ..services import RouteService


class RoutingManager:
    def __init__(self, route_service: RouteService) -> None:
        self.route_service = route_service

    async def route(self, location: str,
                    context: Dict[str, Any] = None) -> Dict[str, Any]:

        return await self.route_service.route(location, context)
