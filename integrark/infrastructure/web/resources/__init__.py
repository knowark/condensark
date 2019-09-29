from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from .graphql import GraphqlResource


class RootResource:

    @template('index.html')
    async def get(self, request):
        return {'version': '0.1.0'}
