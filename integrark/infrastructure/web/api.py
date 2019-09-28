from aiohttp import web
from injectark import Injectark
from .resources import RootResource, GraphqlResource


def create_api(app: web.Application, injector: Injectark) -> None:
    app.router.add_view('/', RootResource)
    app.router.add_view('/graphql', GraphqlResource)
