from aiohttp import web
from injectark import Injectark
from .api import create_api


def create_app(config, injector: Injectark) -> web.Application:
    app = web.Application()

    create_api(app, injector)

    return app
