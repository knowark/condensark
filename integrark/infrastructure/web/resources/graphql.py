from aiohttp import web
from aiohttp_jinja2 import template


class GraphqlResource(web.View):

    @template('playground.html')
    async def get(self):
        return {'version': '0.1.0'}
