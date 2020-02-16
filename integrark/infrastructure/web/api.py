from typing import Any
from aiohttp import web
from injectark import Injectark
from .resources import RootResource, GraphqlResource, RestResource


def create_api(app: web.Application, injector: Injectark) -> None:
    bind_routes(app, '/', RootResource())
    bind_routes(app, '/graphql', GraphqlResource(injector))
    bind_routes(
        app, r'/rest/{location:[^{}/]+}/{path:(.*)}',
        RestResource(injector), 'route')


def bind_routes(app: web.Application, path: str, resource: Any,
                attribute: str = None):
    methods = ['get', 'post', 'put', 'delete', 'patch', 'head']
    for method in methods:
        handler = getattr(resource, attribute or method, None)
        if handler:
            app.router.add_route(method, path, handler)
