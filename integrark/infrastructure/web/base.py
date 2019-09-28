from pathlib import Path
from jinja2 import FileSystemLoader
from aiohttp import web
from aiohttp_jinja2 import setup
from injectark import Injectark
from .api import create_api


def create_app(config, injector: Injectark) -> web.Application:
    app = web.Application()
    templates = str(Path(__file__).parent / 'templates')
    setup(app, loader=FileSystemLoader(templates))
    create_api(app, injector)

    return app


def run_app(app: web.Application, port=4321) -> None:
    web.run_app(app, port=port)
