from aiohttp import web
from injectark import Injectark


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


def create_api(app: web.Application, injector: Injectark) -> None:
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
