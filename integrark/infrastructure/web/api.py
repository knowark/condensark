from typing import Any
from aiohttp import web
from injectark import Injectark
from .resources import RootResource, GraphqlResource


def create_api(app: web.Application, injector: Injectark) -> None:
    bind_routes(app, '/', RootResource())
    bind_routes(app, '/graphql', GraphqlResource(injector))


def bind_routes(app: web.Application, path: str, resource: Any):
    methods = ['get', 'post', 'put', 'delete', 'patch', 'head']
    for method in methods:
        handler = getattr(resource, method, None)
        if handler:
            app.router.add_route(method, path, handler)

