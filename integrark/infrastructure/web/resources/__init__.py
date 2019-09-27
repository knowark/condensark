from aiohttp import web


class RootResource(web.View):

    async def get(self) -> str:
        text = "Welcome to Integrark"
        return web.Response(text=text)
