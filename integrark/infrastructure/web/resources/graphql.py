from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from ....application.coordinators import ExecutionCoordinator


class GraphqlResource:
    def __init__(self, injector: Injectark) -> None:
        self.execution_coordinator: ExecutionCoordinator = injector[
            'ExecutionCoordinator']

    @template('playground.html')
    async def get(self, request):
        return {'version': '0.1.0'}

    async def post(self, request):
        body = await request.text()

        result = await self.execution_coordinator.execute(body)

        return web.json_response(result)
