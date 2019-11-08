from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from .... import __version__
from .graphql import GraphqlResource


class RootResource:

    @template('index.html')
    async def get(self, request):
        return {'version': __version__}
