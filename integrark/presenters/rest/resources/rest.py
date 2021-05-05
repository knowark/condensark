from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from .... import __version__
from ....application.managers import RoutingManager


class RestResource:
    def __init__(self, injector: Injectark) -> None:
        self.routing_manager: RoutingManager = injector[
            'RoutingManager']
        self.injector = injector

    async def route(self, request: web.Request):
        location = request.match_info['location']
        path = request.path_qs.replace(f'/rest/{location}', '')

        context = {
            'method': request.method,
            'url': request.url,
            'request': request,
            'client': request.app['client'],
            'user': request['user'],
            'location': location,
            'path': path,
        }

        result = await self.routing_manager.route(location, context)

        return (result if isinstance(result, web.StreamResponse)
                else web.Response(body=result))
