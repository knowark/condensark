from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from .... import __version__
from ....application.coordinators import RoutingCoordinator


class RestResource:
    def __init__(self, injector: Injectark) -> None:
        self.routing_coordinator: RoutingCoordinator = injector[
            'RoutingCoordinator']
        self.injector = injector

    async def route(self, request: web.Request):
        location = request.match_info['location']
        path = request.path_qs.replace(f'/rest/{location}', '')

        context = {
            'method': request.method,
            'url': request.url,
            'request': request,
            'location': location,
            'path': path,
        }

        result = await self.routing_coordinator.route(location, context)
        if not isinstance(result, web.Response):
            result = web.Response(body=result)

        return result
