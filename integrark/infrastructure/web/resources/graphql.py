from injectark import Injectark
from aiohttp import web
from aiohttp_jinja2 import template
from ....application.coordinators import ExecutionCoordinator


class GraphqlResource:
    def __init__(self, injector: Injectark) -> None:
        self.execution_coordinator: ExecutionCoordinator = injector[
            'ExecutionCoordinator']
        self.context = {
            'injector': injector
        }

    @template('playground.html')
    async def get(self, request):
        return {'version': '0.1.0'}

    async def post(self, request):
        context = self.context
        payload = await request.json()
        operation = payload.get('operationName', '')
        variables = payload.get('variables', {})
        query = payload.get('query', '')

        result = await self.execution_coordinator.execute(query, context)

        return web.json_response(result)
