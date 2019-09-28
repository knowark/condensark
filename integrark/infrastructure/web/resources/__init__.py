from aiohttp import web
from aiohttp_jinja2 import template
from .graphql import GraphqlResource


class RootResource(web.View):

    @template('index.html')
    async def get(self):
        return {'version': '0.1.0'}
