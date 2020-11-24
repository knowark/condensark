from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web
from aiohttp_jinja2 import setup
from injectark import Injectark
from .api import create_api
from .middleware import middlewares
from .generators import setup_generators


def create_app(config, injector: Injectark) -> web.Application:
    app = web.Application(middlewares=middlewares(injector))
    templates = str(Path(__file__).parent / 'templates')
    setup(app, loader=FileSystemLoader(templates))
    setup_generators(app)
    create_api(app, injector)

    return app


async def run_app(app: web.Application, port=4321) -> None:
    await web._run_app(app, port=port)
